package absolutelyaya.ultracraft.registry;

import absolutelyaya.ultracraft.Ultracraft;
import absolutelyaya.ultracraft.advancement.ChargebackCriterion;
import absolutelyaya.ultracraft.advancement.CoinPunchCriterion;
import absolutelyaya.ultracraft.advancement.RicochetCriterion;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;

public class CriteriaRegistry
{
	public static final CoinPunchCriterion COIN_PUNCH = Registry.register(Registries.CRITERION, Ultracraft.identifier("coin_punching"), new CoinPunchCriterion());
	public static final ChargebackCriterion CHARGEBACK = Registry.register(Registries.CRITERION, Ultracraft.identifier("chargeback"), new ChargebackCriterion());
	public static final RicochetCriterion RICOCHET = Registry.register(Registries.CRITERION, Ultracraft.identifier("ricochet"), new RicochetCriterion());

	public static void register()
	{
	}
}
