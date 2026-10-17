import {trait} from "koota";
import {MAGOS_BIOLOGIS_SHEET, type SpriteSheetDef} from "@/common/defs/spriteSheets.ts";

export const SpriteAnimation = trait(() => ({
    sheet: MAGOS_BIOLOGIS_SHEET as SpriteSheetDef,
    clip: "idle",
    time: 0,
    frame: 0,
    flipX: false,
}));
