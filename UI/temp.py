elif self.controller == "Switch":
                        if event.type == pygame.JOYBUTTONDOWN:
                            ACTIONS["interact"] = event.button == SWITCH["interact"]
                            ACTIONS["run"] = event.button == SWITCH["run"]
                            ACTIONS["shoot"] = event.button == SWITCH["shoot"]
                            ACTIONS["element"] = event.button == SWITCH["element"]
                            ACTIONS["pause"] = event.button == SWITCH["pause"]
                            ACTIONS["map"] = event.button == SWITCH["map"]
                            if event.button == SWITCH["target"]:
                                ACTIONS["target"] = True

                        elif event.type == pygame.JOYBUTTONUP:
                            button = event.button
                            if button == SWITCH["interact"]:
                                ACTIONS["interact"] = False
                            elif button == SWITCH["run"]:
                                ACTIONS["run"] = False
                            elif button == SWITCH["shoot"]:
                                ACTIONS["shoot"] = False
                            elif button == SWITCH["element"]:
                                ACTIONS["element"] = False
                            elif button == SWITCH["pause"]:
                                ACTIONS["pause"] = False
                            elif button == SWITCH["map"]:
                                ACTIONS["map"] = False
                            elif button == SWITCH["target"]:
                                ACTIONS["target"] = False

                        elif event.type == pygame.JOYAXISMOTION:
                            if event.value <= self.deadZone:
                                ACTIONS["motion"] = False
                            ACTIONS["motion"] = True
                            ACTIONS["motion_axis"] = event.axis
                            ACTIONS["motion_value"] = event.value
                            if event.axis == 1:
                                ##Upwards
                                if event.value < 0:
                                    if event.value < -self.deadZone:
                                        ACTIONS["up"] = True
                                        ACTIONS["down"] = False
                                    else:
                                        ACTIONS["up"] = False
                                        ACTIONS["down"] = False
                                
                                ##Downwards
                                elif event.value > 0:
                                    if event.value > self.deadZone:
                                        ACTIONS["down"] = True
                                        ACTIONS["up"] = False
                                    else:
                                        ACTIONS["down"] = False
                                        ACTIONS["up"] = False
                                
                                else:
                                    ACTIONS["up"] = False
                                    ACTIONS["down"] = False
                          

                            elif event.axis == 0:
                                ##Leftwards
                                if event.value < 0:
                                    if event.value < -self.deadZone:
                                        ACTIONS["left"] = True
                                        ACTIONS["right"] = False
                                    else:
                                        ACTIONS["left"] = False
                                        ACTIONS["right"] = False
                                
                                ##Rightwards
                                elif event.value > 0:
                                    if event.value > self.deadZone:
                                        ACTIONS["right"] = True
                                        ACTIONS["left"] = False
                                    else:
                                        ACTIONS["right"] = False
                                        ACTIONS["left"] = False

                                else:
                                    ACTIONS["left"] = False
                                    ACTIONS["right"] = False