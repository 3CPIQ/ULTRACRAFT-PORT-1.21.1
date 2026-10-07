package absolutelyaya.ultracraft.particle;

import absolutelyaya.ultracraft.registry.ParticleRegistry;
import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.PacketCodec;
import net.minecraft.network.codec.PacketCodecs;
import net.minecraft.particle.ParticleEffect;
import net.minecraft.particle.ParticleType;

public class TeleportParticleEffect implements ParticleEffect
{
	public static final MapCodec<TeleportParticleEffect> CODEC = Codec.DOUBLE.fieldOf("size")
			.xmap(TeleportParticleEffect::new, TeleportParticleEffect::getSize);
	public static final PacketCodec<ByteBuf, TeleportParticleEffect> PACKET_CODEC = PacketCodecs.DOUBLE
			.xmap(TeleportParticleEffect::new, TeleportParticleEffect::getSize);

	double size;

	public TeleportParticleEffect(double size)
	{
		this.size = size;
	}

	public double getSize()
	{
		return size;
	}

	@Override
	public ParticleType<?> getType()
	{
		return ParticleRegistry.TELEPORT;
	}
}
