from os import listdir
from os.path import isfile, join
import pygame as pg


class InputFileError(Exception):
    pass
class NoInputFileFound(InputFileError):
    pass
class InputFileOverflow(InputFileError):
    pass

class FlightData():

    def __init__(self, APP):
        print("Recolting flights data...")

        self.app = APP
        self.input_files = [f[:21] for f in listdir(join('..', 'my_flights'))]

        l = len(self.input_files)
        if l == 0:
            pg.quit()
            raise NoInputFileFound("Can't find flight file (.igc). Make sure you placed it in app/my_flights folder.")

        if l >= 20:
            pg.quit()
            raise InputFileOverflow("Flight files exceed 20. Please remove some.")

        print(f"Got {len(self.input_files)}")




    def get_new_files(self):
        already_known = [f[:21] for f in listdir("track")]
        return [f for f in self.input_files if not f in already_known]

    @staticmethod
    def convert_LatLon_TO_swissLatLon(lat, lon):
            arcsecLat, arcsecLon = lat*60*60, lon*60*60
            phi, lamb = (arcsecLat - 169028.66)/10000, (arcsecLon - 26782.5)/10000

            E = 2600072.37 + 211455.93 * lamb - 10938.51 * lamb * phi - 0.36 * lamb * phi**2 - 44.54 * lamb**3
            N = 1200147.07 + 308807.95 * phi + 3745.25 * lamb**2 + 76.63 * phi**2 - 194.56 * lamb**2 * phi + 119.79 * phi**3
            return N, E

    def parth_new_files(self):
        new_files = self.get_new_files()
        for file_name in new_files:
            print(f"{file_name}, new flight")
            with open(join('..','my_flights', file_name + '.igc'), 'r') as read_file:
                with open(join("track", file_name + "_parthed.igc"), "w") as write_file:

                    for line in read_file:
                        if line[0] != "B":
                            continue
                        phi_deg = float(line[7:9])
                        phi_min = float(line[9:14])/1000
                        lamb_deg = float(line[15:18])
                        lamb_min = float(line[18:23])/1000
                        alt = float(line[30:35])

                        N, E = self.convert_LatLon_TO_swissLatLon(phi_deg + phi_min/60, lamb_deg + lamb_min/60)

                        l = line[0:7] + " " +line[7:15] + " " + line[15:25] + " " + line[30:35] + "\n"

                        write_file.write(str(E) + " " + str(N) + " " + str(alt) + "\n")
                        #write_file.write(line)
        l = len(new_files)
        if l > 0:
            print(f"{l} new files parthed !")
