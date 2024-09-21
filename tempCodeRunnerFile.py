            player.dir = Vector(
                [
                    mouse_pos[0] - player.pos.x * Values.get_value("CELL_SIZE"),
                    mouse_pos[1] - player.pos.y * Values.get_value("CELL_SIZE"),
                ]
            ).normalise()
