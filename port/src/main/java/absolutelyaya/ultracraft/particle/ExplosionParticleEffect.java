package absolutelyaya.ultracraft.particle;

import absolutelyaya.ultracraft.registry.ParticleRegistry;
import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.PacketCodec;
import net.minecraft.network.codec.PacketCodecs;
import net.minecraft.particle.ParticleEffect;
import net.minecraft.particle.ParticleType;

public class ExplosionParticleEffect implements ParticleEffect
{
	public static final MapCodec<ExplosionParticleEffect> CODEC = Codec.DOUBLE.fieldOf("size")
			.xmap(ExplosionParticleEffect::new, ExplosionParticleEffect::getSize);
	public static final PacketCodec<ByteBuf, ExplosionParticleEffect> PACKET_CODEC = PacketCodecs.DOUBLE
			.xmap(ExplosionParticleEffect::new, ExplosionParticleEffect::getSize);

	double size;

	public ExplosionParticleEffect(double size)
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
		return ParticleRegistry.EXPLOSION;
	}
}
