if event.axis == 3:
                                ##Upwards
                                if event.value < 0:
                                    if event.value < -self.deadZone:
                                        ACTIONS["up_r"] = True
                                        ACTIONS["down_r"] = False
                                    else:
                                        ACTIONS["up_r"] = False
                                        ACTIONS["down_r"] = False
                                
                                ##Downwards
                                elif event.value > 0:
                                    if event.value > self.deadZone:
                                        ACTIONS["down_r"] = True
                                        ACTIONS["up_r"] = False
                                    else:
                                        ACTIONS["down_r"] = False
                                        ACTIONS["up_r"] = False
                                
                                else:
                                    ACTIONS["up_r"] = False
                                    ACTIONS["down_r"] = False
                          

                            elif event.axis == 2:
                                ##Leftwards
                                if event.value < 0:
                                    if event.value < -self.deadZone:
                                        ACTIONS["left_r"] = True
                                        ACTIONS["right_r"] = False
                                    else:
                                        ACTIONS["left_r"] = False
                                        ACTIONS["right_r"] = False
                                
                                ##Rightwards
                                elif event.value > 0:
                                    if event.value > self.deadZone:
                                        ACTIONS["right_r"] = True
                                        ACTIONS["left_r"] = False
                                    else:
                                        ACTIONS["right_r"] = False
                                        ACTIONS["left_r"] = False

                                else:
                                    ACTIONS["left_r"] = False
                                    ACTIONS["right_r"] = False