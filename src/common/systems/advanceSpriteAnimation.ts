import type {World} from "koota";
import {SpriteAnimation} from "@/common/traits/SpriteAnimation.ts";

export const advanceSpriteAnimation = (world: World, delta: number) => {
    world.query(SpriteAnimation).updateEach(([anim]) => {
        const clip = anim.sheet.clips[anim.clip];
        if (!clip) return;

        anim.time += delta;
        const frame = Math.floor(anim.time * clip.fps);
        anim.frame = clip.loop ? frame % clip.frames : Math.min(frame, clip.frames - 1);
    });
}
