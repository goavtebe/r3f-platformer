import {useQueryFirst} from "koota/react";
import {IsPlayer} from "@/common/traits/IsPlayer.ts";
import type {Entity} from "koota";
import {CharacterStartPosition} from "@/common/traits/CharacterStartPosition.ts";
import {useThreeInjector} from "@/common/hooks/injection/useThreeInjector.ts";
import {useCharacterControllerInjector} from "@/common/hooks/injection/useCharacterControllerInjector.ts";
import {INTERACTION_GROUPS} from "@/common/defs/colGroup.ts";
import {useMaterialInjector} from "@/common/hooks/injection/useMaterialInjector.ts";
import useRapier from "@/common/hooks/physics/useRapier.ts";
import useCreateCollider from "@/common/hooks/physics/useCreateCollider.ts";
import {useTexture} from "@react-three/drei";
import {useMemo} from "react";
import * as THREE from "three";
import {getSafePath} from "@/common/utils/electronUtils.ts";
import {SpriteAnimation} from "@/common/traits/SpriteAnimation.ts";
import {PPU} from "@/common/defs/ppu.ts";

const COLLIDER_HALF_EXTENTS = {x: 0.4, y: 0.4};

const PlayerView = ({entity}: { entity: Entity }) => {

    const startPos = entity.get(CharacterStartPosition)!;

    const threeRef = useThreeInjector(entity);
    const materialRef = useMaterialInjector(entity);

    const {sheet} = entity.get(SpriteAnimation)!;
    const sheetTexture = useTexture(getSafePath(sheet.src));
    const spriteTexture = useMemo(() => {
        const texture = sheetTexture.clone();
        texture.magFilter = THREE.NearestFilter;
        texture.minFilter = THREE.NearestFilter;
        texture.generateMipmaps = false;
        texture.wrapS = THREE.ClampToEdgeWrapping;
        texture.wrapT = THREE.ClampToEdgeWrapping;
        texture.needsUpdate = true;
        return texture;
    }, [sheetTexture]);
    const spriteSize = sheet.cellSize / PPU;

    const {rapier} = useRapier();
    const collider = useCreateCollider({
        startPosition: startPos.clone(),
        colliderDesc: rapier.ColliderDesc.cuboid(COLLIDER_HALF_EXTENTS.x, COLLIDER_HALF_EXTENTS.y)
            .setCollisionGroups(INTERACTION_GROUPS.WHITE)
            .setMass(1)
            .setRestitution(0)
            .setFriction(1),
    });
    useCharacterControllerInjector(entity, collider!);

    return <group ref={threeRef}>
        {/* feet sit on the bottom edge of each sprite cell, align them with the collider bottom */}
        <mesh position-y={spriteSize / 2 - COLLIDER_HALF_EXTENTS.y}>
            <planeGeometry args={[spriteSize, spriteSize]}/>
            <meshLambertMaterial color={"white"} map={spriteTexture} alphaTest={0.5} ref={materialRef}/>
        </mesh>
        <pointLight castShadow position-z={2} intensity={2} decay={.5} distance={15} shadow-mapSize-width={256} shadow-mapSize-height={256} shadow-bias={0.005} shadow-normalBias={0.02}/>
    </group>
}

export default function PlayerRenderer() {

    const player = useQueryFirst(IsPlayer);

    if (!player) {
        return <></>;
    }

    return <PlayerView entity={player}/>
}