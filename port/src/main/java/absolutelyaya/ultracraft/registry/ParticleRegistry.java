package absolutelyaya.ultracraft.registry;

import absolutelyaya.ultracraft.Ultracraft;
import absolutelyaya.ultracraft.particle.ExplosionParticleEffect;
import absolutelyaya.ultracraft.particle.ParryIndicatorParticleEffect;
import absolutelyaya.ultracraft.particle.TeleportParticleEffect;
import net.fabricmc.fabric.api.particle.v1.FabricParticleTypes;
import net.minecraft.particle.ParticleType;
import net.minecraft.particle.SimpleParticleType;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;

public class ParticleRegistry
{
	public static final SimpleParticleType MALICIOUS_CHARGE = Registry.register(Registries.PARTICLE_TYPE, Ultracraft.identifier("malicious_charge"), FabricParticleTypes.simple());
	public static final SimpleParticleType DASH = Registry.register(Registries.PARTICLE_TYPE, Ultracraft.identifier("dash"), FabricParticleTypes.simple());
	public static final SimpleParticleType SLIDE = Registry.register(Registries.PARTICLE_TYPE, Ultracraft.identifier("slide"), FabricParticleTypes.simple());
	public static final SimpleParticleType GROUND_POUND = Registry.register(Registries.PARTICLE_TYPE, Ultracraft.identifier("groundpound"), FabricParticleTypes.simple());
	public static final SimpleParticleType EJECTED_CORE_FLASH = Registry.register(Registries.PARTICLE_TYPE, Ultracraft.identifier("ejected_core"), FabricParticleTypes.simple());
	public static final SimpleParticleType BLOOD_SPLASH = Registry.register(Registries.PARTICLE_TYPE, Ultracraft.identifier("blood_splash"), FabricParticleTypes.simple());
	public static final SimpleParticleType BLOOD_BUBBLE = Registry.register(Registries.PARTICLE_TYPE, Ultracraft.identifier("blood_bubble"), FabricParticleTypes.simple());
	public static final SimpleParticleType SOAP_BUBBLE = Registry.register(Registries.PARTICLE_TYPE, Ultracraft.identifier("soap_bubble"), FabricParticleTypes.simple());
	public static final SimpleParticleType RIPPLE = Registry.register(Registries.PARTICLE_TYPE, Ultracraft.identifier("ripple"), FabricParticleTypes.simple());
	public static final SimpleParticleType RICOCHET_WARNING = Registry.register(Registries.PARTICLE_TYPE, Ultracraft.identifier("ricochet_warning"), FabricParticleTypes.simple());
	public static final SimpleParticleType BIG_CIRCLE = Registry.register(Registries.PARTICLE_TYPE, Ultracraft.identifier("bigcircle"), FabricParticleTypes.simple());
	public static final SimpleParticleType DRONE_CHARGE = Registry.register(Registries.PARTICLE_TYPE, Ultracraft.identifier("drone_charge"), FabricParticleTypes.simple());
	public static final SimpleParticleType SHOCK = Registry.register(Registries.PARTICLE_TYPE, Ultracraft.identifier("shock"), FabricParticleTypes.simple());
	public static final SimpleParticleType BUTTERFLY = Registry.register(Registries.PARTICLE_TYPE, Ultracraft.identifier("butterfly"), FabricParticleTypes.simple());

	public static final ParticleType<ParryIndicatorParticleEffect> PARRY_INDICATOR = Registry.register(Registries.PARTICLE_TYPE,
			Ultracraft.identifier("parry_indicator"), FabricParticleTypes.complex(ParryIndicatorParticleEffect.CODEC, ParryIndicatorParticleEffect.PACKET_CODEC));
	public static final ParticleType<TeleportParticleEffect> TELEPORT = Registry.register(Registries.PARTICLE_TYPE,
			Ultracraft.identifier("teleport"), FabricParticleTypes.complex(TeleportParticleEffect.CODEC, TeleportParticleEffect.PACKET_CODEC));
	public static final ParticleType<ExplosionParticleEffect> EXPLOSION = Registry.register(Registries.PARTICLE_TYPE,
			Ultracraft.identifier("explosion"), FabricParticleTypes.complex(ExplosionParticleEffect.CODEC, ExplosionParticleEffect.PACKET_CODEC));

	public static void init()
	{
	}
}
