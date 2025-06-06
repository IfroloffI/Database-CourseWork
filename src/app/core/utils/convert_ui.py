import sys
from pathlib import Path
from PyQt6 import uic
from app.core.config import AppConfig

AppConfig.validate()


class UIConverter:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.ui_dir = self.project_root.parent / "design" / "ui"
        self.generated_dir = self.project_root.parent / "design" / "generated"

    def convert(self):
        try:
            ui_file = self.ui_dir / AppConfig.UI_FILE
            output_file = self.generated_dir / f"ui_{ui_file.stem}.py"

            self._validate_paths(ui_file)
            self._run_conversion(ui_file, output_file)

            print(f"✅ Success: {ui_file.name} → {output_file.name}")
            return True

        except Exception as e:
            print(f"❌ Error: {e}", file=sys.stderr)
            return False

    def _validate_paths(self, ui_file: Path):
        if not ui_file.exists():
            available = [f.name for f in self.ui_dir.glob("*.ui")]
            raise FileNotFoundError(
                f"UI file {ui_file.name} not found in: {self.ui_dir}\n"
                f"Available files: {', '.join(available) or 'no .ui files found'}"
            )

        self.generated_dir.mkdir(parents=True, exist_ok=True)

    def _run_conversion(self, ui_file: Path, output_file: Path):
        try:
            with open(ui_file, "r", encoding="utf-8") as ui_f:
                ui_content = ui_f.read()

            from io import StringIO
            from PyQt6.uic import compileUi

            buf = StringIO()
            compileUi(StringIO(ui_content), buf)
            generated_code = buf.getvalue()

            with open(output_file, "w", encoding="utf-8") as out_f:
                out_f.write(generated_code)

        except Exception as e:
            raise RuntimeError(f"UI compilation failed: {str(e)}")


if __name__ == "__main__":
    converter = UIConverter()
    sys.exit(0 if converter.convert() else 1)
