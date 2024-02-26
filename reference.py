presumed_chr_scale = [('a','f'),('a','n'),('b','f'),('b','n'),('c','n'),('c','s'),('d','n'),('e','f'),('e','n'),('f','n'),('f','s'),('g','n')]

notenames = ['a','b','c','d','e','f','g']

enharm_equivs = [(('g','ss'),('a','n'),('b','ff')),
                     (('a','s'),('b','f'),('c','ff')),
                     (('a','ss'),('b','n'),('c','f')),
                     (('b','s'),('c','n'),('d','ff')),
                     (('b','ss'),('c','s'),('d','f')),
                     (('c','ss'),('d','n'),('e','ff')),
                     (('d','s'),('e','f'),('f','ff')),
                     (('d','ss'),('e','n'),('f','f')),
                     (('e','s'),('f','n'),('g','ff')),
                     (('e','ss'),('f','s'),('g','f')),
                     (('f','ss'),('g','n'),('a','ff')),
                     (('g','s'),('a','f'),('b','fff'))]

sigtokeymap = {'0s': (('c', 'n'), ('a', 'n')), '1s': (('g', 'n'), ('e', 'n')), '2s': (('d', 'n'), ('b', 'n')), '3s': (('a', 'n'), ('f', 's')), '4s': (('e', 'n'), ('c', 's')), '5s': (('b', 'n'), ('g', 's')), '6s': (('f', 's'), ('d', 's')), '7s': (('c', 's'), ('a', 's')), '0f': (('c', 'n'), ('a', 'n')), '1f': (('f', 'n'), ('d', 'n')), '2f': (('b', 'f'), ('g', 'n')), '3f': (('e', 'f'), ('c', 'n')), '4f': (('a', 'f'), ('f', 'n')), '5f': (('d', 'f'), ('b', 'f')), '6f': (('g', 'f'), ('e', 'f')), '7f': (('c', 'f'), ('a', 'f'))}

all_keysigs = {"sharps":{'0s':(),
                      '1s':('f'),
                      '2s':('f','c'),
                      '3s':('f','c','g'),
                      '4s':('f','c','g','d'),
                      '5s':('f','c','g','d','a'),
                      '6s':('f','c','g','d','a','e'),
                      '7s':('f','c','g','d','a','e','b')},
            "flats":{'0f':(),
                     '1f':('b'),
                     '2f':('b','e'),
                     '3f':('b','e','a'),
                     '4f':('b','e','a','d'),
                     '5f':('b','e','a','d','g'),
                     '6f':('b','e','a','d','g','c'),
                     '7f':('b','e','a','d','g','c','f')}
                    }
                   
leadingnotemap = {('a', 'n'): ('g', 's'), ('a', 's'): ('g', 'ss'), ('b', 'f'): ('a', 'n'), ('b', 'n'): ('a', 's'), ('c', 'f'): ('b', 'f'), ('b', 's'): ('a', 'ss'), ('c', 'n'): ('b', 'n'), ('c', 's'): ('b', 's'), ('d', 'f'): ('c', 'n'), ('d', 'n'): ('c', 's'), ('d', 's'): ('c', 'ss'), ('e', 'f'): ('d', 'n'), ('e', 'n'): ('d', 's'), ('f', 'f'): ('e', 'f'), ('e', 's'): ('d', 'ss'), ('f', 'n'): ('e', 'n'), ('f', 's'): ('e', 's'), ('g', 'f'): ('f', 'n'), ('g', 'n'): ('f', 's'), ('g', 's'): ('f', 'ss'), ('a', 'f'): ('g', 'n')}
     
diatonics = {'0s': {1, 3, 4, 6, 8, 9, 11, 13, 15, 16, 18, 20, 21, 23, 25, 27, 28, 30, 32, 33, 35, 37, 39, 40, 42, 44, 45, 47, 49, 51, 52, 54, 56, 57, 59, 61, 63, 64, 66, 68, 69, 71, 73, 75, 76, 78, 80, 81, 83, 85, 87}, '1s': {1, 3, 4, 6, 8, 10, 11, 13, 15, 16, 18, 20, 22, 23, 25, 27, 28, 30, 32, 34, 35, 37, 39, 40, 42, 44, 46, 47, 49, 51, 52, 54, 56, 58, 59, 61, 63, 64, 66, 68, 70, 71, 73, 75, 76, 78, 80, 82, 83, 85, 87}, '2s': {1, 3, 5, 6, 8, 10, 11, 13, 15, 17, 18, 20, 22, 23, 25, 27, 29, 30, 32, 34, 35, 37, 39, 41, 42, 44, 46, 47, 49, 51, 53, 54, 56, 58, 59, 61, 63, 65, 66, 68, 70, 71, 73, 75, 77, 78, 80, 82, 83, 85, 87}, '3s': {1, 3, 5, 6, 8, 10, 12, 13, 15, 17, 18, 20, 22, 24, 25, 27, 29, 30, 32, 34, 36, 37, 39, 41, 42, 44, 46, 48, 49, 51, 53, 54, 56, 58, 60, 61, 63, 65, 66, 68, 70, 72, 73, 75, 77, 78, 80, 82, 84, 85, 87}, '4s': {1, 3, 5, 7, 8, 10, 12, 13, 15, 17, 19, 20, 22, 24, 25, 27, 29, 31, 32, 34, 36, 37, 39, 41, 43, 44, 46, 48, 49, 51, 53, 55, 56, 58, 60, 61, 63, 65, 67, 68, 70, 72, 73, 75, 77, 79, 80, 82, 84, 85, 87}, '5s': {2, 3, 5, 7, 8, 10, 12, 14, 15, 17, 19, 20, 22, 24, 26, 27, 29, 31, 32, 34, 36, 38, 39, 41, 43, 44, 46, 48, 50, 51, 53, 55, 56, 58, 60, 62, 63, 65, 67, 68, 70, 72, 74, 75, 77, 79, 80, 82, 84, 86, 87}, '6s': {2, 3, 5, 7, 9, 10, 12, 14, 15, 17, 19, 21, 22, 24, 26, 27, 29, 31, 33, 34, 36, 38, 39, 41, 43, 45, 46, 48, 50, 51, 53, 55, 57, 58, 60, 62, 63, 65, 67, 69, 70, 72, 74, 75, 77, 79, 81, 82, 84, 86, 87}, '7s': {5, 7, 9, 10, 12, 14, 16, 17, 19, 21, 22, 24, 26, 28, 29, 31, 33, 34, 36, 38, 40, 41, 43, 45, 46, 48, 50, 52, 53, 55, 57, 58, 60, 62, 64, 65, 67, 69, 70, 72, 74, 76, 77, 79, 81, 82, 84, 86}, '0f': {1, 3, 4, 6, 8, 9, 11, 13, 15, 16, 18, 20, 21, 23, 25, 27, 28, 30, 32, 33, 35, 37, 39, 40, 42, 44, 45, 47, 49, 51, 52, 54, 56, 57, 59, 61, 63, 64, 66, 68, 69, 71, 73, 75, 76, 78, 80, 81, 83, 85, 87}, '1f': {1, 2, 4, 6, 8, 9, 11, 13, 14, 16, 18, 20, 21, 23, 25, 26, 28, 30, 32, 33, 35, 37, 38, 40, 42, 44, 45, 47, 49, 50, 52, 54, 56, 57, 59, 61, 62, 64, 66, 68, 69, 71, 73, 74, 76, 78, 80, 81, 83, 85, 86}, '2f': {1, 2, 4, 6, 7, 9, 11, 13, 14, 16, 18, 19, 21, 23, 25, 26, 28, 30, 31, 33, 35, 37, 38, 40, 42, 43, 45, 47, 49, 50, 52, 54, 55, 57, 59, 61, 62, 64, 66, 67, 69, 71, 73, 74, 76, 78, 79, 81, 83, 85, 86}, '3f': {2, 4, 6, 7, 9, 11, 12, 14, 16, 18, 19, 21, 23, 24, 26, 28, 30, 31, 33, 35, 36, 38, 40, 42, 43, 45, 47, 48, 50, 52, 54, 55, 57, 59, 60, 62, 64, 66, 67, 69, 71, 72, 74, 76, 78, 79, 81, 83, 84, 86}, '4f': {2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24, 26, 28, 29, 31, 33, 35, 36, 38, 40, 41, 43, 45, 47, 48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84, 86}, '5f': {2, 4, 5, 7, 9, 10, 12, 14, 16, 17, 19, 21, 22, 24, 26, 28, 29, 31, 33, 34, 36, 38, 40, 41, 43, 45, 46, 48, 50, 52, 53, 55, 57, 58, 60, 62, 64, 65, 67, 69, 70, 72, 74, 76, 77, 79, 81, 82, 84, 86}, '6f': {2, 3, 5, 7, 9, 10, 12, 14, 15, 17, 19, 21, 22, 24, 26, 27, 29, 31, 33, 34, 36, 38, 39, 41, 43, 45, 46, 48, 50, 51, 53, 55, 57, 58, 60, 62, 63, 65, 67, 69, 70, 72, 74, 75, 77, 79, 81, 82, 84, 86, 87}, '7f': {2, 3, 5, 7, 8, 10, 12, 14, 15, 17, 19, 20, 22, 24, 26, 27, 29, 31, 32, 34, 36, 38, 39, 41, 43, 44, 46, 48, 50, 51, 53, 55, 56, 58, 60, 62, 63, 65, 67, 68, 70, 72, 74, 75, 77, 79, 80, 82, 84, 86}}
