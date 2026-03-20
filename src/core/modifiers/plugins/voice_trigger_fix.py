"""VoiceTrigger fix plugin.

This plugin ensures VoiceTrigger is correctly placed on older Android versions.
"""

import shutil
from pathlib import Path

from src.core.modifiers.plugin_system import ModifierPlugin, ModifierRegistry


@ModifierRegistry.register
class VoiceTriggerFixPlugin(ModifierPlugin):
    """Plugin to fix VoiceTrigger placement on Android < 16."""

    name = "voice_trigger_fix"
    description = "Fix VoiceTrigger placement for Android < 16"
    priority = 35

    def modify(self) -> bool:
        """Apply VoiceTrigger fix."""
        # Get base Android version
        base_android_version = getattr(self.ctx, "base_android_version", "0")

        # Only apply to Android < 16
        try:
            if int(base_android_version) >= 16:
                self.logger.debug(f"Skipping VoiceTrigger fix: Android version {base_android_version} >= 16")
                return True
        except (ValueError, TypeError):
            self.logger.warning(f"Invalid Android version: {base_android_version}")
            return True

        # Paths
        stock_vt_dir = self.ctx.stock.extracted_dir / "product/app/VoiceTrigger"
        target_product_vt_dir = self.ctx.target_dir / "product/app/VoiceTrigger"
        target_system_ext_vt_dir = self.ctx.target_dir / "system_ext/app/VoiceTrigger"

        # Check if stock has VoiceTrigger
        if not stock_vt_dir.exists():
            self.logger.info("Stock does not have VoiceTrigger, skipping fix")
            return True

        # Copy from stock to system_ext
        self.logger.info(f"Moving VoiceTrigger from stock to {target_system_ext_vt_dir}")
        if target_system_ext_vt_dir.exists():
            shutil.rmtree(target_system_ext_vt_dir)

        target_system_ext_vt_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(stock_vt_dir, target_system_ext_vt_dir)

        # Remove from product if it exists in target
        if target_product_vt_dir.exists():
            self.logger.info(f"Removing VoiceTrigger from {target_product_vt_dir}")
            shutil.rmtree(target_product_vt_dir)

        return True
