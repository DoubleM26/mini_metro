from constants import BG_COLOR
import pygame


class Line:
    def __init__(self, color):
        self.color = color
        self.ends = [(0, 0), (0, 0)]
        self.fragments = []
        self.used_bridges = 0
    
    def set_ends(self, fp, sp, stations):
        if self.ends == [(0, 0), (0, 0)]:
            self.ends[0], self.ends[1] = fp, sp
            stations.colors[fp[1] // 36][fp[0] // 36] = self.color
        elif fp == self.ends[0]:
            self.ends[0] = sp
        elif fp == self.ends[1]:
            self.ends[1] = sp
    
    def add_fragment(self, fp, sp, stations, panel, basic_rivers, screen, myfont):
        print(self.color, fp, sp, "  ends:", self.ends)
        if stations.colors[sp[1] // 36][sp[0] // 36] == self.color:
            print("kuku", stations.colors[sp[1] // 36][sp[0] // 36], self.color)
            return

        if self.ends[0] == fp or self.ends[1] == fp or self.ends == [(0, 0), (0, 0)]:
            for river in basic_rivers:
                if pygame.draw.line(screen, BG_COLOR, fp, sp) \
                        .colliderect(river):
                    if panel.bridges.bridge_count > 0:
                        self.set_ends(fp, sp, stations)
                        self.fragments.append((fp, sp))
                        stations.colors[sp[1] // 36][sp[0] // 36] = self.color
                        panel.bridges.bridge_count -= 1
                        self.used_bridges += 1
                        panel.bridge_number = myfont.render(
                            str(panel.bridges.bridge_count), False, (255, 255, 255))
                    break
            else:
                self.set_ends(fp, sp, stations)
                stations.colors[sp[1] // 36][sp[0] // 36] = self.color
                self.fragments.append((fp, sp))
        for el in stations.colors:
            print(*el)

    def clear(self, panel, myfont):
        self.ends = [(0, 0), (0, 0)]
        self.fragments = []
        panel.bridges.bridge_count += self.used_bridges
        self.used_bridges = 0
        panel.bridge_number = myfont.render(
            str(panel.bridges.bridge_count), False, (255, 255, 255))
