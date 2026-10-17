import type {World} from "koota";
import {IsPlayer} from "@/common/traits/IsPlayer.ts";
import {MoveInput} from "@/common/traits/MoveInput.ts";
import {CharacterAirTime, CharacterVelocity} from "@/common/traits/CharacterValues.ts";
import {CharacterControllerRef} from "@/common/traits/CharacterControllerRef.ts";
import {SpriteAnimation} from "@/common/traits/SpriteAnimation.ts";
import type {PlayerAnimationClip} from "@/common/defs/spriteSheets.ts";

const AIRBORNE_GRACE = 0.08;

export const updatePlayerAnimationClip = (world: World, delta: number) => {
    world.query(IsPlayer, MoveInput, CharacterVelocity, CharacterControllerRef, CharacterAirTime, SpriteAnimation)
        .updateEach(([, moveInput, vel, ctrl, airTime, anim]) => {
            airTime.time = ctrl.isGrounded ? 0 : airTime.time + delta;

            let clip: PlayerAnimationClip;
            if (airTime.time > AIRBORNE_GRACE) {
                clip = vel.y > 0 ? "jump" : "fall";
            } else if (moveInput.x !== 0) {
                clip = "run";
            } else {
                clip = "idle";
            }

            if (anim.clip !== clip) {
                anim.clip = clip;
                anim.time = 0;
                anim.frame = 0;
            }
            if (moveInput.x !== 0) {
                anim.flipX = moveInput.x < 0;
            }
        });
}
