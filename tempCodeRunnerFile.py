it_ray = Ray.refractRay(TIR_hit, TIR_ray.intensity, going_to_air=True)

                    # print(exit_ray)
                    # exit_hit = exit_ray.cast(game_map, refracting=True)

                    # draw_fading_ray(
                    #     screen,
                    #     exit_ray.pos,
                    #     exit_hit.pos,
                    #     alpha_start=exit_ray.intensity,
                    #     alpha_end=exit_ray.intensity / Values.get_value("Decay_Factor"),
                    #     segments=50,
                    # )

                    # curr_hit = exit_hit
