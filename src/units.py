
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

   def target(self, opponent, atk_up, armor_up, shield_up=0):
      for i in range(self.volleys):
         opponent.take_hit(atk_up * self.per_up + self.dmg, armor_up, shield_up)

class Unit:
   def __init__(self, names, attrs, hp, mins=0, gas=0, attacks=[], shields=0, \
                armor=0, per_up=1):
      self.names = names
      self.name = names[0]
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
         return false
      
      attack.target(opponent, atk_up, armor_up, shield_up)
      return True
   
   def take_hit(self, dmg, armor_up, shield_up=0):
#TODO: How does base armor work with Protoss?
      if self.shields > 0:
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
      attrs='glbp',
      hp=300, shields=100,
      attacks=[
         Attack('Warp Blade (v. armored)', 110, 1.2, 'ga'),
         Attack('Warp Blade', 85, 1.2, 'g'),
      ]
   ), Unit(
      names=['probe'],
      attrs='glm',
      mins=50,
      hp=20, shields=20,
      attacks=[
         Attack('Particle Beam', 5, 1.5, 'g'),
      ]
   ), Unit(
      names=['zealot', 'lot'],
      attrs='glb', 
      hp=100, shields=50,
      attacks=[
         Attack('Psi Blade', 8, 1.2, 'g', volleys=2),
      ]
   ), Unit(
      names=['stalker'],
      attrs='gam',
      hp=100, shields=50,
      attacks=[
         Attack('Particle Disruptor (v. armored)', 14, 1.44, 'gfa'),
         Attack('Particle Disruptor', 10, 1.44, 'gf'),
      ]
   ), Unit(
      names=['sentry'],
      attrs='glmp',
      hp=40, shields=40,
      attacks=[
         Attack('Disruption Beam', 6, 1, 'gf'),
      ]
   ), Unit(
#TODO: Hardened Shields
      names=['immortal','immo'],
      attrs='gam',
      hp=200, shields=100,
      attacks=[
         Attack('Phase Disruptor (v. armored)', 50, 1.45, 'ga', per_up=3),
         Attack('Phase Disruptor', 20, 1.45, 'g', per_up=2),
      ]
   ), Unit(
      names=['colossus','colossi'],
      attrs='gfamv',
      hp=200, shields=150,
      armor=1,
      attacks=[
         Attack('Thermal Lance', 15, 1.65, 'g', per_up=2, volleys=2, splash=True),
      ]
   ), Unit(
      names=['warpprism','wp'],
      attrs='famp',
      hp=100, shields=100,
      attacks=[
      ]
   ), Unit(
      names=['observer','obs'],
      attrs='flm',
      hp=40, shields=20,
      attacks=[
      ]
   ), Unit(
      names=['hightemplar','ht'],
      attrs='glbp',
      hp=40, shields=40,
      attacks=[
         Attack('Psi Storm', 80, 4, 'gf', per_up=0, splash=True),
      ]
   ), Unit(
      names=['darktemplar','dt'],
      attrs='glbp',
      hp=40, shields=80,
      armor=1,
      attacks=[
         Attack('Warp Blade', 45, 1.694, 'g', per_up=5),
      ]
   ), Unit(
      names=['archon'],
      attrs='gpv',
      hp=10, shields=350,
      attacks=[
         Attack('Psionic Shockwave (v. biological)', 35, 1.754, 'gfb', per_up=1, splash=True),
         Attack('Psionic Shockwave', 25, 1.754, 'gf', per_up=3, splash=True),
      ]
   ), Unit(
      names=['phoenix','penix'],
      attrs='flm',
      hp=120, shields=60,
      attacks=[
#TODO: Can't attack massive... but not a big deal.
         Attack('Ion Cannon (v. light)', 10, 1.11, 'gfb', volleys=2),
         Attack('Ion Cannon', 5, 1.11, 'gf', volleys=2),
      ]
   ), Unit(
      names=['voidray','vr'],
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
      attrs='famv',
      hp=300, shields=250,
      armor=2,
   ), Unit(
      names=['interceptor'],
      attrs='flm',
      hp=40, shields=40,
      attacks=[
         Attack('Interceptor Beam', 5, 3, 'gf', volleys=2),
      ]
   ), Unit(
      names=['mothership','mommaship'],
      attrs='famv',
      hp=350, shields=350,
      armor=2,
      attacks=[
         Attack('Purifier Beam', 6, 2.21, 'gf', volleys=6),
      ]
   ), Unit(
      names=['tempest'],
      attrs='famv',
      hp=300, shields=150,
      attacks=[
         Attack('LAZAR BEEM (v. massive)', 60, 6, 'gfv'),
         Attack('LAZAR BEEM', 45, 6, 'gfv'),
      ]
   ), Unit(
      names=['oracle'],
      attrs='flm',
      hp=80, shields=20,
   ), Unit(
      names=['cannon'],
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
      attrs='glb',
      hp=25,
      armor=10,
      per_up=0,
   ), Unit(
      names=['drone'],
      attrs='glb',
      hp=40,
      attacks=[
         Attack('Claw', 5, 1.5, 'g'),
      ]
   ), Unit(
      names=['zergling','ling'],
      attrs='glb',
      hp=35,
      attacks=[
         Attack('Claw', 5, 0.696, 'g'),
      ]
   ), Unit(
      names=['crackling'],
      attrs='glb',
      hp=35,
      attacks=[
         Attack('Claw', 5, 0.587, 'g'),
      ]
   ), Unit(
      names=['baneling','bling'],
      attrs='gb',
      hp=30,
      attacks=[
         Attack('Attack Building', 80, 0.833, 'g', per_up=5, splash=True),
         Attack('Volatile Burst (v. light)', 35, 0.833, 'g', per_up=4,splash=True),
         Attack('Volatile Burst', 20, 0.833, 'g', per_up=2, splash=True),
      ]
   ), Unit(
      names=['queen'],
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
      attrs='gab',
      hp=145,
      armor=1,
      attacks=[
         Attack('Acid Saliva', 16, 2, 'g', per_up=2),
      ]
   ), Unit(
      names=['hydralisk','hydra'],
      attrs='glb',
      hp=80,
      attacks=[
         Attack('Needle Spine', 12, 0.83, 'gf'),
      ]
   ), Unit(
      names=['infestor'],
      attrs='gabp',
      hp=90,
      attacks=[
#TODO: Currently takes armor into account, but shouldn't.
         Attack('Fungal Growth (v. armored)', 40, 4, 'gfa', per_up=0),
         Attack('Fungal Growth', 30, 4, 'gf', per_up=0),
      ]
   ), Unit(
      names=['infestedterran','infested','infested-terran'],
      attrs='glb',
      hp=50,
      attacks=[
         Attack('Infested Gauss Rifle', 8, 0.8608, 'gf'),
      ]
   ), Unit(
      names=['mutalisk','muta'],
      attrs='flb',
      hp=120,
      attacks=[
         Attack('Glaive Wurm', 9, 1.5246, 'gf'),
      ]
   ), Unit(
      names=['corruptor'],
      attrs='fab',
      hp=200,
      attacks=[
         Attack('Parasite Spore (v. massive)', 20, 1.9, 'fv', per_up=2),
         Attack('Parasite Spore', 14, 1.9, 'f'),
      ]
   ), Unit(
      names=['mutalisk','muta'],
      attrs='flb',
      hp=120,
      attacks=[
         Attack('Glaive Wurm', 9, 1.5246, 'gf'),
      ]
   ), Unit(
      names=['broodlord','brood','bl','brood-lord'],
      attrs='fabv',
      hp=225,
      attacks=[
         Attack('Broodling Strike', 20, 2.5, 'g', volleys=2, per_up=2),
      ]
   ), Unit(
      names=['broodling'],
      attrs='glb',
      hp=30,
      attacks=[
         Attack('Claws', 6, 0.6455, 'g'),
      ]
   ), Unit(
      names=['ultralisk','ultra'],
      attrs='gabv',
      hp=500,
      attacks=[
         Attack('Kaiser Blade (v. armored)', 20, 0.861, 'ga', per_up=2, splash=True),
         Attack('Kaiser Blade', 15, 0.861, 'g', per_up=2, splash=True),
      ]
   ), Unit(
      names=['spinecrawler','spine','spine-crawler'],
      attrs='gabs',
      hp=300,
      armor=2,
      per_up=0,
      attacks=[
         Attack('Impaler Tentacle (v. armored)', 30, 1.85, 'ga'),
         Attack('Impaler Tentacle', 25, 1.85, 'g'),
      ]
   ), Unit(
      names=['sporecrawler','spore','spore-crawler'],
      attrs='gabs',
      hp=400,
      armor=1,
      per_up=0,
      attacks=[
         Attack('Seeker Spore', 15, 0.8608, 'f'),
      ]
   ), Unit(
      names=['overlord','ol'],
      attrs='gabs',
      hp=200,
      per_up=0, #?
   ), Unit(
      names=['viper'],
      attrs='fab',
      hp=120,
   ), Unit(
      names=['swarmhost'],
      attrs='gab',
      hp=120,
   ), Unit(
      names=['locust'],
      attrs='gb',
      hp=110,
      attacks=[
         Attack('Locust Attack', 14, 0.8608, 'gf'),
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
   if attacker.can_attack(defender):
      count = 0
      defender.reset_health()
      while defender.hp > 0:
         attacker.attack(defender, atk_up, armor_up, shield_up)
         count += 1
      return count
   
   return -1
