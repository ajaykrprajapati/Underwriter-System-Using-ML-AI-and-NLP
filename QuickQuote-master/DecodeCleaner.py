# -*- coding: utf-8 -*-

import os
os.system(f'''tr -cd "\11\12\15\40-\176" < Data/garbage.csv > Data/raw_data1.csv''')
