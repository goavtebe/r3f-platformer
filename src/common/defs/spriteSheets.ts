export type SpriteClipDef = {
    row: number;
    frames: number;
    fps: number;
    loop: boolean;
};

export type SpriteSheetDef<TClip extends string = string> = {
    src: string;
    cellSize: number;
    columns: number;
    rows: number;
    clips: Record<TClip, SpriteClipDef>;
};

export type PlayerAnimationClip = "idle" | "run" | "jump" | "fall";

export const MAGOS_BIOLOGIS_SHEET: SpriteSheetDef<PlayerAnimationClip> = {
    src: "/assets/sprites/magos-biologis.png",
    cellSize: 32,
    columns: 6,
    rows: 4,
    clips: {
        idle: {row: 0, frames: 4, fps: 5, loop: true},
        run: {row: 1, frames: 6, fps: 12, loop: true},
        jump: {row: 2, frames: 2, fps: 8, loop: false},
        fall: {row: 3, frames: 2, fps: 8, loop: true},
    },
};
