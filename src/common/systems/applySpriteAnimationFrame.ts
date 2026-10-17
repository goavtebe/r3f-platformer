import type {World} from "koota";
import type {MeshLambertMaterial} from "three";
import {SpriteAnimation} from "@/common/traits/SpriteAnimation.ts";
import {MaterialRef} from "@/common/traits/MaterialRef.ts";

export const applySpriteAnimationFrame = (world: World) => {
    world.query(SpriteAnimation, MaterialRef).updateEach(([anim, material]) => {
        const map = (material as MeshLambertMaterial).map;
        const clip = anim.sheet.clips[anim.clip];
        if (!map || !clip) return;

        const cellU = 1 / anim.sheet.columns;
        const cellV = 1 / anim.sheet.rows;
        const u = anim.frame * cellU;
        const v = 1 - (clip.row + 1) * cellV;

        map.repeat.set(anim.flipX ? -cellU : cellU, cellV);
        map.offset.set(anim.flipX ? u + cellU : u, v);
    });
}
