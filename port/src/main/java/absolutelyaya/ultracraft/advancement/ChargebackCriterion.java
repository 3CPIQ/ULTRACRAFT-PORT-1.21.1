package absolutelyaya.ultracraft.advancement;

import absolutelyaya.ultracraft.entity.AbstractUltraHostileEntity;
import absolutelyaya.ultracraft.registry.CriteriaRegistry;
import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.advancement.AdvancementCriterion;
import net.minecraft.advancement.criterion.AbstractCriterion;
import net.minecraft.loot.context.LootContext;
import net.minecraft.predicate.entity.EntityPredicate;
import net.minecraft.predicate.entity.LootContextPredicate;
import net.minecraft.server.network.ServerPlayerEntity;

import java.util.Optional;

public class ChargebackCriterion extends AbstractCriterion<ChargebackCriterion.Conditions>
{
	@Override
	public Codec<Conditions> getConditionsCodec()
	{
		return Conditions.CODEC;
	}

	public void trigger(ServerPlayerEntity player, AbstractUltraHostileEntity victim)
	{
		LootContext context = EntityPredicate.createAdvancementEntityLootContext(player, victim);
		trigger(player, conditions -> conditions.matches(context));
	}

	public record Conditions(Optional<LootContextPredicate> player, Optional<LootContextPredicate> entity) implements AbstractCriterion.Conditions
	{
		public static final Codec<Conditions> CODEC = RecordCodecBuilder.create(instance -> instance.group(
				EntityPredicate.LOOT_CONTEXT_PREDICATE_CODEC.optionalFieldOf("player").forGetter(Conditions::player),
				EntityPredicate.LOOT_CONTEXT_PREDICATE_CODEC.optionalFieldOf("entity").forGetter(Conditions::entity)
		).apply(instance, Conditions::new));

		public static AdvancementCriterion<Conditions> create(EntityPredicate entity)
		{
			return CriteriaRegistry.CHARGEBACK.create(new Conditions(Optional.empty(), Optional.of(EntityPredicate.asLootContextPredicate(entity))));
		}

		public boolean matches(LootContext context)
		{
			return entity.isEmpty() || entity.get().test(context);
		}
	}
}
