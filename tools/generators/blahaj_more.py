# 100 more Blåhaj. name: (display, stripe colors, extra ingredients, category)
def m(x):
    return f"minecraft:{x}"


def d(*names):
    return [f"minecraft:{n}_dye" for n in names]


MORE = {
    # ---- more pride flags
    "progress_pride_blahaj": ("Progress Pride Blåhaj", ["e40303", "ff8c00", "ffed00", "008026", "004dff", "750787", "5bcefa", "f5a9b8"],
                              d("red", "orange", "yellow", "green", "blue", "purple", "light_blue"), "flags2"),
    "transfem_blahaj": ("Transfem Blåhaj", ["73deff", "ffe2ee", "ffb5d6", "b660ff", "ffb5d6", "ffe2ee", "73deff"], d("light_blue", "pink", "purple"), "flags2"),
    "transmasc_blahaj": ("Transmasc Blåhaj", ["ff8abd", "cdf5fe", "9aebff", "74dfff", "9aebff", "cdf5fe", "ff8abd"], d("pink", "light_blue", "cyan"), "flags2"),
    "genderqueer_blahaj": ("Genderqueer Blåhaj", ["b57edc", "ffffff", "4a8123"], d("purple", "white", "green"), "flags2"),
    "bigender_blahaj": ("Bigender Blåhaj", ["c479a2", "eda5cd", "d6c7e8", "ffffff", "d6c7e8", "9ac7e8", "6d82d1"], d("magenta", "pink", "light_blue", "white"), "flags2"),
    "polysexual_blahaj": ("Polysexual Blåhaj", ["f714ba", "01d66a", "1594f6"], d("magenta", "lime", "blue"), "flags2"),
    "omnisexual_blahaj": ("Omnisexual Blåhaj", ["fe9ace", "ff53bf", "200044", "6760fe", "8ea6ff"], d("pink", "magenta", "black", "blue"), "flags2"),
    "aroace_blahaj": ("Aroace Blåhaj", ["e28c00", "eccd00", "ffffff", "62aedc", "203856"], d("orange", "yellow", "white", "light_blue", "blue"), "flags2"),
    "demisexual_blahaj": ("Demisexual Blåhaj", ["000000", "ffffff", "6e0070", "d2d2d2"], d("black", "white", "purple", "light_gray"), "flags2"),
    "demiromantic_blahaj": ("Demiromantic Blåhaj", ["000000", "ffffff", "3da542", "d2d2d2"], d("black", "white", "green", "light_gray"), "flags2"),
    "graysexual_blahaj": ("Graysexual Blåhaj", ["740194", "aeb1aa", "ffffff", "aeb1aa", "740194"], d("purple", "light_gray", "white"), "flags2"),
    "abrosexual_blahaj": ("Abrosexual Blåhaj", ["75ca91", "b3e4c7", "ffffff", "e695b5", "d9446a"], d("lime", "white", "pink", "red"), "flags2"),
    "sapphic_blahaj": ("Sapphic Blåhaj", ["fd8ba8", "fbf2ff", "c76bc5", "fdd768"], d("pink", "white", "magenta", "yellow"), "flags2"),
    "achillean_blahaj": ("Achillean Blåhaj", ["4fae7e", "a5e6c3", "ffffff", "a3d0ec", "5a7fd6"], d("green", "white", "light_blue"), "flags2"),
    "androgyne_blahaj": ("Androgyne Blåhaj", ["fe007f", "9832ff", "00b8e7"], d("magenta", "purple", "cyan"), "flags2"),
    "neutrois_blahaj": ("Neutrois Blåhaj", ["ffffff", "1f9f00", "000000"], d("white", "green", "black"), "flags2"),
    "genderflux_blahaj": ("Genderflux Blåhaj", ["f47694", "f2a2b9", "cecece", "7ce0f7", "3ecdf9", "fff48d"], d("pink", "light_gray", "light_blue", "yellow"), "flags2"),
    "maverique_blahaj": ("Maverique Blåhaj", ["fff42f", "ffffff", "ffa52f"], d("yellow", "white", "orange"), "flags2"),
    "polyamorous_blahaj": ("Polyamorous Blåhaj", ["0000ff", "ff0000", "000000"], d("blue", "red", "black"), "flags2"),
    "pangender_blahaj": ("Pangender Blåhaj", ["fff798", "fedde7", "ffffff", "fedde7", "fff798"], d("yellow", "pink", "white"), "flags2"),
    # ---- food
    "strawberry_blahaj": ("Strawberry Blåhaj", ["e8334f", "ff6b81", "e8334f"], [m("sweet_berries")], "food"),
    "blueberry_blahaj": ("Blueberry Blåhaj", ["3f51b5", "5c6bc0", "3f51b5"], [m("sweet_berries")] + d("blue"), "food"),
    "watermelon_blahaj": ("Watermelon Blåhaj", ["2e7d32", "f8f8f0", "ff5c70", "ff5c70"], [m("melon_slice")], "food"),
    "pumpkin_spice_blahaj": ("Pumpkin Spice Blåhaj", ["c8742c", "e0a060", "8a4b24"], [m("pumpkin_pie")], "food"),
    "apple_blahaj": ("Apple Blåhaj", ["d63a2f", "e8574a"], [m("apple")], "food"),
    "cookie_blahaj": ("Cookie Blåhaj", ["c8935a", "5a3420", "c8935a"], [m("cookie")], "food"),
    "cake_blahaj": ("Cake Blåhaj", ["ffffff", "f5d6b0", "e8334f", "f5d6b0"], [m("cake")], "food"),
    "honey_blahaj": ("Honey Blåhaj", ["f2b22c", "f7cd5b"], [m("honey_bottle")], "food"),
    "glow_berry_blahaj": ("Glow Berry Blåhaj", ["f7a530", "ffd36b", "5e8a3a"], [m("glow_berries")], "food"),
    "mushroom_blahaj": ("Mushroom Blåhaj", ["c62828", "ffffff", "c62828"], [m("red_mushroom")], "food"),
    "cotton_candy_blahaj": ("Cotton Candy Blåhaj", ["ffb3d9", "b3e0ff", "ffb3d9", "b3e0ff"], [m("sugar")] + d("pink", "light_blue"), "food"),
    "mocha_blahaj": ("Mocha Blåhaj", ["6f4a35", "a77b5a"], [m("cocoa_beans")], "food"),
    "mint_chip_blahaj": ("Mint Chip Blåhaj", ["9fe3c4", "4a3020", "9fe3c4"], [m("cocoa_beans")] + d("lime"), "food"),
    "bubblegum_blahaj": ("Bubblegum Blåhaj", ["ff8fc8", "ffb0d8"], [m("slime_ball")] + d("pink"), "food"),
    # ---- minerals
    "emerald_blahaj": ("Emerald Blåhaj", ["17c554", "4fe08a", "17c554"], [m("emerald")], "minerals"),
    "amethyst_blahaj": ("Amethyst Blåhaj", ["9a5cc6", "cfa0f3", "9a5cc6"], [m("amethyst_shard")], "minerals"),
    "copper_blahaj": ("Copper Blåhaj", ["c15a36", "e07c4f", "5db594"], [m("copper_ingot")], "minerals"),
    "iron_blahaj": ("Iron Blåhaj", ["d8d8d8", "aaaaaa"], [m("iron_ingot")], "minerals"),
    "redstone_blahaj": ("Redstone Blåhaj", ["aa0f01", "ff2a00", "aa0f01"], [m("redstone")], "minerals"),
    "lapis_blahaj": ("Lapis Blåhaj", ["1d4fb5", "3a6fe0", "1d4fb5"], [m("lapis_lazuli")], "minerals"),
    "quartz_blahaj": ("Quartz Blåhaj", ["eae5de", "d6cfc6"], [m("quartz")], "minerals"),
    "prismarine_blahaj": ("Prismarine Blåhaj", ["63a597", "8fd1c0", "3f7c70"], [m("prismarine_shard")], "minerals"),
    "resin_blahaj": ("Resin Blåhaj", ["e8731c", "f59a3b"], [m("resin_clump")], "minerals"),
    "echo_blahaj": ("Echo Blåhaj", ["0a3a40", "1f7a80", "0a3a40"], [m("echo_shard")], "minerals"),
    # ---- mobs
    "creeper_blahaj": ("Creeper Blåhaj", ["4caf50", "2e7d32", "4caf50"], [m("gunpowder")], "mobs"),
    "enderman_blahaj": ("Enderman Blåhaj", ["161616", "2a1a2e", "c86bff"], [m("ender_pearl")], "mobs"),
    "slime_blahaj": ("Slime Blåhaj", ["78c850", "a0e070"], [m("slime_ball")], "mobs"),
    "magma_blahaj": ("Magma Blåhaj", ["3a0e05", "ff6a00", "3a0e05"], [m("magma_cream")], "mobs"),
    "blaze_blahaj": ("Blaze Blåhaj", ["ffb000", "ffe066", "ff7a00"], [m("blaze_powder")], "mobs"),
    "wither_blahaj": ("Wither Blåhaj", ["1c1c1c", "3a3a3a"], [m("wither_rose")], "mobs"),
    "axolotl_blahaj": ("Axolotl Blåhaj", ["ffb6d5", "ff8fc0", "ffb6d5"], [m("axolotl_bucket")], "mobs"),
    "frog_blahaj": ("Frog Blåhaj", ["d07e45", "e8b06a", "6a8a3a"], [m("ochre_froglight")], "mobs"),
    "bee_blahaj": ("Bee Blåhaj", ["f7c331", "2a2a2a", "f7c331", "2a2a2a"], [m("honeycomb")], "mobs"),
    "warden_blahaj": ("Warden Blåhaj", ["0d2b35", "1c4f5e", "36d1e0"], [m("sculk")], "mobs"),
    "sniffer_blahaj": ("Sniffer Blåhaj", ["a2362c", "3f8f5a", "a2362c"], [m("torchflower")], "mobs"),
    "squid_blahaj": ("Squid Blåhaj", ["2a3f5f", "3d5a80"], [m("ink_sac")], "mobs"),
    "phantom_blahaj": ("Phantom Blåhaj", ["43518a", "88e070", "43518a"], [m("phantom_membrane")], "mobs"),
    "ghast_blahaj": ("Ghast Blåhaj", ["f2f2f2", "d0d0d0"], [m("ghast_tear")], "mobs"),
    "shulker_blahaj": ("Shulker Blåhaj", ["946a94", "b78bb7"], [m("shulker_shell")], "mobs"),
    "turtle_blahaj": ("Turtle Blåhaj", ["3f8a3a", "6cbf4f", "3f8a3a"], [m("turtle_scute")], "mobs"),
    "armadillo_blahaj": ("Armadillo Blåhaj", ["a66a5a", "d49a86"], [m("armadillo_scute")], "mobs"),
    "breeze_blahaj": ("Breeze Blåhaj", ["9fb4ff", "d6e0ff", "9fb4ff"], [m("breeze_rod")], "mobs"),
    "dragon_blahaj": ("Dragon Blåhaj", ["1a1a1a", "cc44ff", "1a1a1a"], [m("dragon_breath")], "mobs"),
    "panda_blahaj": ("Panda Blåhaj", ["ffffff", "1a1a1a", "ffffff"], [m("bamboo")], "mobs"),
    # ---- nature
    "sakura_blahaj": ("Sakura Blåhaj", ["ffc0d9", "ff99c2", "ffc0d9"], [m("cherry_leaves")], "nature"),
    "sunflower_blahaj": ("Sunflower Blåhaj", ["ffd000", "6b3e1f", "ffd000"], [m("sunflower")], "nature"),
    "lilac_blahaj": ("Lilac Blåhaj", ["c8a2e0", "e0c8f0"], [m("lilac")], "nature"),
    "rose_blahaj": ("Rose Blåhaj", ["c2185b", "e91e63", "2e7d32"], [m("rose_bush")], "nature"),
    "cornflower_blahaj": ("Cornflower Blåhaj", ["4a6fe0", "6f8ff0"], [m("cornflower")], "nature"),
    "lily_blahaj": ("Lily Blåhaj", ["ffffff", "f0f0e0", "3f8a3a"], [m("lily_of_the_valley")], "nature"),
    "tulip_blahaj": ("Tulip Blåhaj", ["f29ac0", "f7bfd8", "3f8a3a"], [m("pink_tulip")], "nature"),
    "moss_blahaj": ("Moss Blåhaj", ["5b7a2e", "79a03c"], [m("moss_block")], "nature"),
    "cactus_blahaj": ("Cactus Blåhaj", ["2f8a3a", "5fb04a", "2f8a3a"], [m("cactus")], "nature"),
    "snow_blahaj": ("Snow Blåhaj", ["ffffff", "e6f0ff"], [m("snowball")], "nature"),
    "ice_blahaj": ("Ice Blåhaj", ["74b4ff", "a8d0ff", "74b4ff"], [m("blue_ice")], "nature"),
    "coral_blahaj": ("Coral Blåhaj", ["ff6fa8", "ffa0c8", "ff6fa8"], [m("brain_coral")], "nature"),
    # ---- sky
    "sunset_blahaj": ("Sunset Blåhaj", ["ff5e3a", "ff9a3a", "ff6fa8", "8a4fc8"], d("orange", "magenta"), "sky"),
    "sunrise_blahaj": ("Sunrise Blåhaj", ["ffd36b", "ffb0a0", "ff8fc0"], d("yellow", "pink"), "sky"),
    "midnight_blahaj": ("Midnight Blåhaj", ["0b1030", "1d2a5a", "0b1030"], d("black", "blue"), "sky"),
    "aurora_blahaj": ("Aurora Blåhaj", ["3ae08a", "3ac8e0", "9a5ce0", "3ae08a"], d("lime", "cyan", "purple"), "sky"),
    "galaxy_blahaj": ("Galaxy Blåhaj", ["1a0b3a", "5a2a9a", "c86bff", "1a0b3a"], d("purple", "black", "white"), "sky"),
    "ocean_blahaj": ("Ocean Blåhaj", ["0f4c81", "1f78b4", "5fc8e0"], d("blue", "cyan"), "sky"),
    "storm_blahaj": ("Storm Blåhaj", ["4a4f5a", "7a808c", "4a4f5a"], d("gray", "light_gray"), "sky"),
    "star_blahaj": ("Star Blåhaj", ["fff6c8", "ffe680", "fff6c8"], [m("nether_star")], "sky"),
    "sun_blahaj": ("Sun Blåhaj", ["ffcc00", "ff9900", "ffcc00"], [m("glowstone_dust")], "sky"),
    "moon_blahaj": ("Moon Blåhaj", ["d8d8e8", "b0b0c8", "d8d8e8"], [m("end_stone")], "sky"),
    # ---- aesthetics
    "vaporwave_blahaj": ("Vaporwave Blåhaj", ["ff71ce", "01cdfe", "05ffa1", "b967ff"], d("pink", "cyan"), "aesthetic"),
    "pastel_goth_blahaj": ("Pastel Goth Blåhaj", ["1a1a1a", "ffb3d9", "1a1a1a"], d("black", "pink"), "aesthetic"),
    "emo_blahaj": ("Emo Blåhaj", ["111111", "c8102e", "111111"], d("black", "red"), "aesthetic"),
    "scene_blahaj": ("Scene Blåhaj", ["39ff14", "ff1493", "111111"], d("lime", "pink", "black"), "aesthetic"),
    "y2k_blahaj": ("Y2K Blåhaj", ["c0c0d8", "ff9ad5", "c0c0d8"], d("light_gray", "pink"), "aesthetic"),
    "cottagecore_blahaj": ("Cottagecore Blåhaj", ["e8d8b0", "a8c890", "f2c4d0"], [m("wheat")], "aesthetic"),
    # ---- elements
    "fire_blahaj": ("Fire Blåhaj", ["ff3d00", "ff9100", "ffd600"], [m("fire_charge")], "elements"),
    "water_blahaj": ("Water Blåhaj", ["2962ff", "448aff", "82b1ff"], [m("water_bucket")], "elements"),
    "earth_blahaj": ("Earth Blåhaj", ["6d4c41", "8d6e63", "558b2f"], [m("dirt")], "elements"),
    "lightning_blahaj": ("Lightning Blåhaj", ["fff176", "ffee58", "5c6bc0"], [m("lightning_rod")], "elements"),
    "void_blahaj": ("Void Blåhaj", ["05030a", "1a0f2e", "05030a"], [m("ender_eye")], "elements"),
    # ---- holidays
    "christmas_blahaj": ("Christmas Blåhaj", ["c62828", "ffffff", "2e7d32"], d("red", "green"), "holidays"),
    "halloween_blahaj": ("Halloween Blåhaj", ["ff8c1a", "1a1a1a", "ff8c1a"], [m("jack_o_lantern")], "holidays"),
    "valentine_blahaj": ("Valentine Blåhaj", ["e8334f", "ff8fb0", "e8334f"], d("red", "pink"), "holidays"),
}
assert len(MORE) == 100, len(MORE)

LIGHT = {"glow_blahaj": 10, "star_blahaj": 12, "sun_blahaj": 15, "fire_blahaj": 8, "blaze_blahaj": 6}
RARE = {"golden_blahaj", "diamond_blahaj", "netherite_blahaj", "glow_blahaj", "star_blahaj", "dragon_blahaj",
        "echo_blahaj", "sun_blahaj", "emerald_blahaj"}
FIRE_RESISTANT = {"netherite_blahaj", "fire_blahaj", "blaze_blahaj", "magma_blahaj"}
SPARKLY = {"golden_blahaj", "diamond_blahaj", "glow_blahaj", "star_blahaj", "galaxy_blahaj", "amethyst_blahaj",
           "emerald_blahaj", "echo_blahaj", "sun_blahaj", "aurora_blahaj", "midnight_blahaj"}
