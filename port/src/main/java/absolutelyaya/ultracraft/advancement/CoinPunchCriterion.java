package absolutelyaya.ultracraft.advancement;

import absolutelyaya.ultracraft.registry.CriteriaRegistry;
import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.advancement.AdvancementCriterion;
import net.minecraft.advancement.criterion.AbstractCriterion;
import net.minecraft.predicate.entity.EntityPredicate;
import net.minecraft.predicate.entity.LootContextPredicate;
import net.minecraft.server.network.ServerPlayerEntity;

import java.util.Optional;

public class CoinPunchCriterion extends AbstractCriterion<CoinPunchCriterion.Conditions>
{
	@Override
	public Codec<Conditions> getConditionsCodec()
	{
		return Conditions.CODEC;
	}

	public void trigger(ServerPlayerEntity player, int score)
	{
		trigger(player, conditions -> conditions.matches(score));
	}

	public record Conditions(Optional<LootContextPredicate> player, int score) implements AbstractCriterion.Conditions
	{
		public static final Codec<Conditions> CODEC = RecordCodecBuilder.create(instance -> instance.group(
				EntityPredicate.LOOT_CONTEXT_PREDICATE_CODEC.optionalFieldOf("player").forGetter(Conditions::player),
				Codec.INT.fieldOf("score").forGetter(Conditions::score)
		).apply(instance, Conditions::new));

		public static AdvancementCriterion<Conditions> create(int score)
		{
			return CriteriaRegistry.COIN_PUNCH.create(new Conditions(Optional.empty(), score));
		}

		public boolean matches(int score)
		{
			return score >= this.score;
		}
	}
}
