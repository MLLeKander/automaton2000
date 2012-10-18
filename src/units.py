
''' Attrs:
    g - ground
    f - flying
    a - armored
    b - biological
    l - light
    v - massive
    m - mechanical
    p - psionic
    s - structure '''
import math


class Attack:
   def __init__(self, name, dmg, cooldown, target_attrs, per_up=1, \
                splash=False, volleys=1):
      self.name = name
      self.dmg = dmg
      self.cooldown = cooldown
      self.per_up = per_up
      self.target_attrs = target_attrs
      self.volleys = volleys
      self.splash = splash
   
   def can_target(self, opponent):
      for attr in list(self.target_attrs):
         if attr not in 'gf' and attr not in opponent.attrs:
            return False
      return 'g' in self.target_attrs and 'g' in opponent.attrs or \
             'f' in self.target_attrs and 'f' in opponent.attrs

   def target(self, opponent, atk_up=0, armor_up=0, shield_up=0):
      for i in range(self.volleys):
         opponent.take_hit(atk_up * self.per_up + self.dmg, armor_up, shield_up)

class Unit:
   def __init__(self, names, race, attrs, hp, mins=0, gas=0, attacks=[], shields=0, \
                armor=0, per_up=1):
      self.names = names
      self.name = names[0]
      self.race = race
      self.attacks = attacks
      self.attrs = attrs
      self.hp = self.max_hp = hp
      self.shields = self.max_shields = shields
      self.armor = armor
      self.per_up = per_up
   
   def can_attack(self, opponent):
      for attack in self.attacks:
         if attack.can_target(opponent):
            return attack
      
      return None
   
   def attack(self, opponent, atk_up=0, armor_up=0, shield_up=0):
      attack = self.can_attack(opponent)
      if not attack:
         return False
      
      attack.target(opponent, atk_up, armor_up, shield_up)
      return True
   
   def take_hit(self, dmg, armor_up, shield_up=0):
	 #TODO: How does base armor work with Protoss?
      if self.shields > 0:
         if self.name == 'immortal' and dmg > 10:
					  dmg = 10
				 else
				    dmg = max(0.5, dmg - shield_up)

         self.shields -= dmg
         if self.shields <= 0:
            dmg = abs(self.shields)
            self.shields = 0
         else:
            return
   
      dmg = max(0.5, dmg - armor_up*self.per_up - self.armor)
      self.hp -= dmg
   
#TODO: So rediculously ugly...
   def reset_health(self):
      self.hp = self.max_hp
      self.shields = self.max_shields

units = [
   # Protoss Units

   Unit(
      names=['zeratul'],
      race='p',
      attrs='glbp',
      hp=300, shields=100,
      attacks=[
         Attack('Warp Blade (v. armored)', 110, 1.2, 'ga'),
         Attack('Warp Blade', 85, 1.2, 'g'),
      ]
   ), Unit(
      names=['probe'],
      race='p',
      attrs='glm',
      mins=50,
      hp=20, shields=20,
      attacks=[
         Attack('Particle Beam', 5, 1.5, 'g'),
      ]
   ), Unit(
      names=['zealot', 'lot'],
      race='p',
      attrs='glb', 
      hp=100, shields=50,
      attacks=[
         Attack('Psi Blade', 8, 1.2, 'g', volleys=2),
      ]
   ), Unit(
      names=['stalker'],
      race='p',
      attrs='gam',
      hp=100, shields=50,
      attacks=[
         Attack('Particle Disruptor (v. armored)', 14, 1.44, 'gfa'),
         Attack('Particle Disruptor', 10, 1.44, 'gf'),
      ]
   ), Unit(
      names=['sentry'],
      race='p',
      attrs='glmp',
      hp=40, shields=40,
      attacks=[
         Attack('Disruption Beam', 6, 1, 'gf'),
      ]
   ), Unit(
#TODO: Hardened Shields
      names=['immortal','immo'],
      race='p',
      attrs='gam',
      hp=200, shields=100,
      attacks=[
         Attack('Phase Disruptor (v. armored)', 50, 1.45, 'ga', per_up=3),
         Attack('Phase Disruptor', 20, 1.45, 'g', per_up=2),
      ]
   ), Unit(
      names=['colossus','colossi'],
      race='p',
      attrs='gfamv',
      hp=200, shields=150,
      armor=1,
      attacks=[
         Attack('Thermal Lance', 15, 1.65, 'g', per_up=2, volleys=2, splash=True),
      ]
   ), Unit(
      names=['warpprism','warp-prism','wp'],
      race='p',
      attrs='famp',
      hp=100, shields=100,
      attacks=[
      ]
   ), Unit(
      names=['observer','obs'],
      race='p',
      attrs='flm',
      hp=40, shields=20,
      attacks=[
      ]
   ), Unit(
      names=['hightemplar','ht'],
      race='p',
      attrs='glbp',
      hp=40, shields=40,
      attacks=[
         Attack('Psi Storm', 80, 4, 'gf', per_up=0, splash=True),
      ]
   ), Unit(
      names=['darktemplar','dt'],
      race='p',
      attrs='glbp',
      hp=40, shields=80,
      armor=1,
      attacks=[
         Attack('Warp Blade', 45, 1.694, 'g', per_up=5),
      ]
   ), Unit(
      names=['archon'],
      race='p',
      attrs='gpv',
      hp=10, shields=350,
      attacks=[
         Attack('Psionic Shockwave (v. biological)', 35, 1.754, 'gfb', per_up=1, splash=True),
         Attack('Psionic Shockwave', 25, 1.754, 'gf', per_up=3, splash=True),
      ]
   ), Unit(
      names=['phoenix','penix'],
      race='p',
      attrs='flm',
      hp=120, shields=60,
      attacks=[
#TODO: Can't attack massive... but not a big deal.
         Attack('Ion Cannon (v. light)', 10, 1.11, 'gfl', volleys=2),
         Attack('Ion Cannon', 5, 1.11, 'gf', volleys=2),
      ]
   ), Unit(
      names=['voidray','void-ray','vr'],
      race='p',
      attrs='fam',
      hp=100, shields=150,
      attacks=[
#TODO: Not sure how to handle all cases. Assume fully charged for now.
         Attack('Prismatic Beam (v. massive armored)', 19, 0.6, 'gfav'),
         Attack('Prismatic Beam (v. armored)', 16, 0.6, 'gfa'),
         Attack('Prismatic Beam (v. massive)', 10, 0.6, 'gfv'),
         Attack('Prismatic Beam', 8, 0.6, 'gf'),
      ]
   ), Unit(
      names=['carrier'],
      race='p',
      attrs='famv',
      hp=300, shields=250,
      armor=2,
   ), Unit(
      names=['interceptor'],
      race='p',
      attrs='flm',
      hp=40, shields=40,
      attacks=[
         Attack('Interceptor Beam', 5, 3, 'gf', volleys=2),
      ]
   ), Unit(
      names=['mothership','mother-ship','mommaship'],
      race='p',
      attrs='famv',
      hp=350, shields=350,
      armor=2,
      attacks=[
         Attack('Purifier Beam', 6, 2.21, 'gf', volleys=6),
      ]
   ), Unit(
      names=['tempest'],
      race='p',
      attrs='famv',
      hp=300, shields=150,
      armor=1,
      attacks=[
         Attack('Storm Sphere (v. massive)', 50, 3.3, 'gfv'),
         Attack('Storm Sphere', 30, 3.3, 'gfv'),
      ]
   ), Unit(
      names=['oracle'],
      race='p',
      attrs='flm',
      hp=80, shields=20,
   ), Unit(
      names=['photoncannon','photon-cannon','cannon'],
      race='p',
      attrs='gams',
      hp=150, shields=150,
      armor=1,
      per_up=0,
      attacks=[
         Attack('Phase Disruptor', 20, 1.25, 'gf', per_up=1),
      ]
   ),
   
   #Zerg Units
   
   Unit(
      names=['larva','larvae'],
      race='z',
      attrs='glb',
      hp=25,
      armor=10,
      per_up=0,
   ), Unit(
      names=['drone'],
      race='z',
      attrs='glb',
      hp=40,
      attacks=[
         Attack('Claw', 5, 1.5, 'g'),
      ]
   ), Unit(
      names=['zergling','ling'],
      race='z',
      attrs='glb',
      hp=35,
      attacks=[
         Attack('Claw', 5, 0.696, 'g'),
      ]
   ), Unit(
      names=['crackling'],
      race='z',
      attrs='glb',
      hp=35,
      attacks=[
         Attack('Claw', 5, 0.587, 'g'),
      ]
   ), Unit(
      names=['baneling','bling','bane'],
      race='z',
      attrs='gb',
      hp=30,
      attacks=[
         Attack('Attack Building', 80, 0.833, 'gs', per_up=5, splash=True),
         Attack('Volatile Burst (v. light)', 35, 0.833, 'gl', per_up=4,splash=True),
         Attack('Volatile Burst', 20, 0.833, 'g', per_up=2, splash=True),
      ]
   ), Unit(
      names=['queen'],
      race='z',
      attrs='gbp',
      hp=175,
      armor=1,
      attacks=[
#TODO: Maybe just cut cooldown in half and make 1 volley?
         Attack('Claws', 4, 1, 'g', volleys=2),
         Attack('Acid Spine', 9, 1, 'f'),
      ]
   ), Unit(
      names=['roach'],
      race='z',
      attrs='gab',
      hp=145,
      armor=1,
      attacks=[
         Attack('Acid Saliva', 16, 2, 'g', per_up=2),
      ]
   ), Unit(
      names=['hydralisk','hydra'],
      race='z',
      attrs='glb',
      hp=80,
      attacks=[
         Attack('Needle Spine', 12, 0.83, 'gf'),
      ]
   ), Unit(
      names=['infestor'],
      race='z',
      attrs='gabp',
      hp=90,
      attacks=[
#TODO: Currently takes armor into account, but shouldn't.
         Attack('Fungal Growth (v. armored)', 40, 4, 'gfa', per_up=0),
         Attack('Fungal Growth', 30, 4, 'gf', per_up=0),
      ]
   ), Unit(
      names=['infestedterran','infested-terran','infested'],
      race='z',
      attrs='glb',
      hp=50,
      attacks=[
         Attack('Infested Gauss Rifle', 8, 0.8608, 'gf'),
      ]
   ), Unit(
      names=['mutalisk','muta'],
      race='z',
      attrs='flb',
      hp=120,
      attacks=[
         Attack('Glaive Wurm', 9, 1.5246, 'gf'),
      ]
   ), Unit(
      names=['corruptor'],
      race='z',
      attrs='fab',
      hp=200,
      attacks=[
         Attack('Parasite Spore (v. massive)', 20, 1.9, 'fv', per_up=2),
         Attack('Parasite Spore', 14, 1.9, 'f'),
      ]
   ), Unit(
      names=['mutalisk','muta'],
      race='z',
      attrs='flb',
      hp=120,
      attacks=[
         Attack('Glaive Wurm', 9, 1.5246, 'gf'),
      ]
   ), Unit(
      names=['broodlord','brood-lord','brood','bl'],
      race='z',
      attrs='fabv',
      hp=225,
      attacks=[
         Attack('Broodling Strike', 20, 2.5, 'g', volleys=2, per_up=2),
      ]
   ), Unit(
      names=['broodling'],
      race='z',
      attrs='glb',
      hp=30,
      attacks=[
         Attack('Claws', 6, 0.6455, 'g'),
      ]
   ), Unit(
      names=['ultralisk','ultra'],
      race='z',
      attrs='gabv',
      hp=500,
      attacks=[
         Attack('Kaiser Blade (v. armored)', 20, 0.861, 'ga', per_up=2, splash=True),
         Attack('Kaiser Blade', 15, 0.861, 'g', per_up=2, splash=True),
      ]
   ), Unit(
      names=['spinecrawler','spine-crawler','spine'],
      race='z',
      attrs='gabs',
      hp=300,
      armor=2,
      per_up=0,
      attacks=[
         Attack('Impaler Tentacle (v. armored)', 30, 1.85, 'ga'),
         Attack('Impaler Tentacle', 25, 1.85, 'g'),
      ]
   ), Unit(
      names=['sporecrawler','spore-crawler','spore'],
      race='z',
      attrs='gabs',
      hp=400,
      armor=1,
      per_up=0,
      attacks=[
         Attack('Seeker Spore', 15, 0.8608, 'f'),
      ]
   ), Unit(
      names=['overlord','over-lord','ol'],
      race='z',
      attrs='gabs',
      hp=200,
      per_up=0, #?
   ), Unit(
      names=['viper'],
      race='z',
      attrs='fab',
      hp=120,
   ), Unit(
      names=['swarmhost', 'swarm-host'],
      race='z',
      attrs='gab',
      hp=120,
   ), Unit(
      names=['locust'],
      race='z',
      attrs='glb',
      hp=65,
      attacks=[
          # TODO: Real attack name?
          Attack('Locust Attack', 14, 0.8608, 'g'),
      ]
   ),

   # Terran Units

   Unit(
      names=['SCV'],
      race='t',
      attrs='glm',
      hp=45,
      attacks=[
         Attack('Fusion Cutter', 5, 1.5, 'g'),
      ]
   ), Unit(
      names=['MULE'],
      race='t',
      attrs='glm',
      hp=60,
   ), Unit(
      names=['marine'],
      race='t',
      attrs='glb',
      hp=45,
      attacks=[
         Attack('C-14 Rifle', 6, 0.8608, 'gf'),
      ]
   ), Unit(
      names=['combat-shielded-marine', 'csmarine', 'combatmarine', 'combat-marine'],
      race='t',
      attrs='glb',
      hp=55,
      attacks=[
         Attack('C-14 Rifle', 6, 0.8608, 'gf'),
      ]
   ), Unit(
      names=['stimpack-marine', 'stimmarine', 'stim-marine', 'stimmedmarine', 'stimmed-marine'],
      race='t',
      attrs='glb',
      hp=45,
      attacks=[
         Attack('C-14 Rifle (w/ stim)', 6, 0.5739, 'gf'),
      ]
   ), Unit(
      names=['marauder'],
      race='t',
      attrs='gab',
      hp=125,
      armor=1,
      attacks=[
         Attack('Punisher Grenade (v. armored)', 20, 1.5, 'ga'),
         Attack('Punisher Grenade', 10, 1.5, 'g'),
      ]
   ), Unit(
      names=['stimpack-marauder', 'stimmarauder', 'stim-marauder', 'stimmedmarauder', 'stimmed-marauder'],
      race='t',
      attrs='gab',
      hp=125,
      armor=1,
      attacks=[
         Attack('Punisher Grenade (v. armored, w/ stim)', 20, 1, 'ga'),
         Attack('Punisher Grenade (w/ stim)', 10, 1, 'g'),
      ]
   ), Unit(
      names=['reaper'],
      race='t',
      attrs='glb',
      hp=50,
      attacks=[
         Attack('D-8 Charges', 30, 1.8, 'gb'),
         Attack('P-38 Reaper pistol (v. light)', 9, 1.1, 'gl'),
         Attack('P-38 Reaper pistol', 4, 1.1, 'g'),
      ]
   ), Unit(
      names=['ghost'],
      race='t',
      attrs='gpb',
      hp=100,
      attacks=[
         Attack('C-10 Rifle (v. light)', 20, 1.5, 'gfl'),
         Attack('C-10 Rifle', 10, 1.5, 'gfl'),
      ]
   ), Unit(
      names=['hellion'],
      race='t',
      attrs='glm',
      hp=90,
      attacks=[
         Attack('Infernal Flamethrower (v. light)', 14, 2.5, 'gl'),
         Attack('Infernal Flamethrower', 8, 2.5, 'g'),
      ]
   ), Unit(
      names=['blue-flame-hellion', 'blueflamehellion', 'bfhellion'],
      race='t',
      attrs='glm',
      hp=90,
      attacks=[
         Attack('Infernal Flamethrower (v. light)', 19, 2.5, 'gl'),
         Attack('Infernal Flamethrower', 8, 2.5, 'g'),
      ]
   ), Unit(
      names=['tank'],
      race='t',
      attrs='gam',
      hp=160,
      armor=1,
      attacks=[
         Attack('90 mm Twin Cannon (v. armored)', 25, 1.04, 'ga', per_up=3),
         Attack('90 mm Twin Cannon', 15, 1.04, 'g', per_up=2),
      ]
   ), Unit(
      names=['siege-tank','siegetank'],
      race='t',
      attrs='gam',
      hp=160,
      armor=1,
      attacks=[
         Attack('120 mm Shock Cannon (v. armored)', 50, 3, 'ga', per_up=5, splash=True),
         Attack('120 mm Shock Cannon', 35, 3, 'g', per_up=3, splash=True),
      ]
   ), Unit(
      names=['thor'],
      race='t',
      attrs='gamv',
      hp=400,
      armor=1,
      attacks=[
         Attack('Thor\'s Hammer', 30, 1.28, 'g', per_up=3, volleys=2),
         Attack('Javelin Missile (v. light)', 12, 3, 'fl', volleys=4, splash=True),
         Attack('Javelin Missile', 6, 3, 'f', volleys=4, splash=True),
      ]
   ), Unit(
      names=['viking'],
      race='t',
      attrs='fam',
      hp=125,
      attacks=[
         Attack('Lanzer Torpedo (v. armored)', 14, 2, 'f', per_up=2, volleys=2),
         Attack('Lanzer Torpedo', 10, 2, 'f', volleys=2),
         Attack('Twin Gatling Cannon', 12, 1, 'g'),
      ]
   ), Unit(
      names=['medivac'],
      race='t',
      attrs='fam',
      hp=150,
   ), Unit(
      names=['raven'],
      race='t',
      attrs='flm',
      hp=140,
      armor=1,
   ), Unit(
      names=['pointdefensedrone','point-defense-drone','pdd'],
      race='t',
      attrs='flmb',
      hp=50,
      per_up=2,
   ), Unit(
      names=['seekermissile','seeker-missile','hunterseeker','hsm'],
      race='t',
      attrs='',
      hp=1,
      attacks=[
         Attack('Seeker Missile', 100, 0, 'gf'),
      ]
   ), Unit(
      names=['autoturret','auto-turret'],
      race='t',
      attrs='gams',
      hp=150,
      armor=1,
      attacks=[
         Attack('12mm Gauss Cannon', 8, 0.8, 'gf'),
      ]
   ), Unit(
      names=['banshee'],
      race='t',
      attrs='flm',
      hp=140,
      attacks=[
         Attack('Backlash Rocket', 12, 1.25, 'g', volleys=2),
      ]
   ), Unit(
      names=['battlecruiser','battle-cruiser','cattlebruiser','bc'],
      race='t',
      attrs='famv',
      hp=550,
      armor=3,
      attacks=[
         Attack('ATS Laser Battery (v. air)', 6, 0.225, 'f'),
         Attack('ATS Laser Battery (v. ground)', 8, 0.225, 'f'),
      ]
   ), Unit(
      names=['planetaryfortress','planetary-fortress','pf'],
      race='t',
      attrs='gams',
      hp=1500,
      armor=3,
      attacks=[
         Attack('Ibiks Cannon', 40, 2, 'g', splash=True),
      ]
   ), Unit(
      names=['missileturret','missile-turret','turret'],
      race='t',
      attrs='gams',
      hp=250,
      attacks=[
         Attack('Longbolt Missile', 12, 0.8608, 'f', volleys=2),
      ]
   ),
]

def get_unit(name):
   name = name.lower()
   for unit in units:
      if name in unit.names:
         return unit
   
   return None

def htk(attacker, defender, atk_up=0, armor_up=0, shield_up=0):
   attack = attacker.can_attack(defender)
   if attack:
      count = 0
      defender.reset_health()
      regen = 0
      
      while defender.hp > 0:
         attack.target(defender, atk_up, armor_up, shield_up)
         if defender.race == 'z':
            regen += 0.27 * attack.cooldown
            if regen >= 1:
               defender.hp += math.floor(regen)
               regen -= math.floor(regen)
         count += 1
      return count
   
   return -1
