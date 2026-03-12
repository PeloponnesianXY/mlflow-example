import argparse
import os
import shutil

import mlflow
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from mlflow_local import MODEL_STAGING_DIR, configure_runtime, configure_tracking


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train Fashion-MNIST with PyTorch + MLflow")
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--lr", type=float, default=1e-3)
    return parser.parse_args()


class FashionNet(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28 * 28, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 10),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def evaluate(model: nn.Module, loader: DataLoader, loss_fn: nn.Module, device: torch.device) -> tuple[float, float]:
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            logits = model(x)
            loss = loss_fn(logits, y)
            total_loss += loss.item() * x.size(0)
            preds = logits.argmax(dim=1)
            correct += (preds == y).sum().item()
            total += x.size(0)
    return total_loss / total, correct / total


def main() -> None:
    args = parse_args()
    configure_runtime()
    configure_tracking("fashion-mnist")
    device = torch.device("cpu")

    transform = transforms.ToTensor()
    train_ds = datasets.FashionMNIST(root="data", train=True, download=True, transform=transform)
    test_ds = datasets.FashionMNIST(root="data", train=False, download=True, transform=transform)
    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=args.batch_size)

    model = FashionNet().to(device)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    with mlflow.start_run() as run:
        mlflow.log_params({"epochs": args.epochs, "batch_size": args.batch_size, "lr": args.lr})

        for epoch in range(1, args.epochs + 1):
            model.train()
            total_loss = 0.0
            total = 0
            for x, y in train_loader:
                x, y = x.to(device), y.to(device)
                optimizer.zero_grad()
                logits = model(x)
                loss = loss_fn(logits, y)
                loss.backward()
                optimizer.step()
                total_loss += loss.item() * x.size(0)
                total += x.size(0)

            train_loss = total_loss / total
            test_loss, test_acc = evaluate(model, test_loader, loss_fn, device)

            mlflow.log_metric("train_loss", train_loss, step=epoch)
            mlflow.log_metric("test_loss", test_loss, step=epoch)
            mlflow.log_metric("test_accuracy", test_acc, step=epoch)
            print(f"epoch={epoch} train_loss={train_loss:.4f} test_loss={test_loss:.4f} test_acc={test_acc:.4f}")

        model_dir = os.path.join(MODEL_STAGING_DIR, run.info.run_id, "model")
        if os.path.exists(model_dir):
            shutil.rmtree(model_dir)
        os.makedirs(os.path.dirname(model_dir), exist_ok=True)
        mlflow.pytorch.save_model(model, model_dir)
        mlflow.log_artifacts(model_dir, artifact_path="model")


if __name__ == "__main__":
    main()
