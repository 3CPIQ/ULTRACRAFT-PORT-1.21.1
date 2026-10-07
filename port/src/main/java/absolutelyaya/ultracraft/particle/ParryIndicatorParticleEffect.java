package absolutelyaya.ultracraft.particle;

import absolutelyaya.ultracraft.registry.ParticleRegistry;
import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.PacketCodec;
import net.minecraft.network.codec.PacketCodecs;
import net.minecraft.particle.ParticleEffect;
import net.minecraft.particle.ParticleType;
import net.minecraft.registry.Registries;

public class ParryIndicatorParticleEffect implements ParticleEffect
{
	public static final MapCodec<ParryIndicatorParticleEffect> CODEC = Codec.BOOL.fieldOf("unparriable")
			.xmap(ParryIndicatorParticleEffect::new, ParryIndicatorParticleEffect::isUnparriable);
	public static final PacketCodec<ByteBuf, ParryIndicatorParticleEffect> PACKET_CODEC = PacketCodecs.BOOL
			.xmap(ParryIndicatorParticleEffect::new, ParryIndicatorParticleEffect::isUnparriable);

	final boolean unparriable;

	public ParryIndicatorParticleEffect(boolean unparriable)
	{
		this.unparriable = unparriable;
	}

	public boolean isUnparriable()
	{
		return unparriable;
	}

	@Override
	public ParticleType<?> getType()
	{
		return ParticleRegistry.PARRY_INDICATOR;
	}

	@Override
	public String toString()
	{
		return String.format("%s %s", Registries.PARTICLE_TYPE.getId(getType()), unparriable);
	}
}
