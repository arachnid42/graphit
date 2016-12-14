import csv
import sys

class UnknownError(Exception):
    """ Indicates that parser failed to initialize because of unknown reason """
    pass


class NoFilesFound(Exception):
    """ Indicates that parser was unable to locate input files to parse """
    pass


class MPParser(object):
    """ Class that holds a parser for a Metec's master plan """

    def __init__(self, mp_csv_path, peg_csv_path, debug=False):
        """ Initializes parser and fetches files into reader objects

        :param mp_csv_path - string path to .CSV file that holds
               a master plan
        :param peg_csv_path - string path to .CSV file that holds
               a PEG file

        """

        self.debug = debug
        try:
            self.mp_f = open(mp_csv_path, 'rU', newline='', encoding='windows-1252')  # damn Microsoft
            self.peg_f = open(peg_csv_path, 'rU', newline='', encoding='windows-1252')
            self.mp_reader = csv.reader(self.mp_f, delimiter=';', quotechar='"')
            self.peg_reader = csv.reader(self.peg_f, delimiter=',', quotechar='"')
        except FileNotFoundError:
            raise NoFilesFound("Unable to locate input files to parse!")
        except:
            raise UnknownError("Parser failed to initialize!")

    def parse(self):
        """ Generator that parses input and returns lists of necessary data one by one

        :yield list - [<string_source_department_label>,
                        <string _destination_department_label>,
                        <int_quantity_of_transported_items>,
                        <string_date_of_transportation>]

        """

        # skipping headers
        next(self.mp_reader, None)
        next(self.peg_reader, None)

        # dictionary to save parsed data
        # {<src_opcode>,<dest_opcode>] -> [<src_dep>,<dest_dep>,<time>,<quantity>}
        data = {}
        # mapper to use for appending missing destination information
        # {<dest_opcode> -> [<src_opcode_1>, <src_opcode_2>, ...]}
        mapper = {}

        if self.debug:
            ind = 2

        # stage 1: iterating over all rows of master plan
        for mp_row in self.mp_reader:

            # fill missed destination labels
            try:
                for src_opcode in mapper[mp_row[0].strip()]:
                    data[(src_opcode.strip(), mp_row[0].strip())][1] = mp_row[8]
            except KeyError:
                pass

            # can be skipped as there is no interest in this kind of data
            if mp_row[6] == "DefaultSalesResource" or mp_row[10] == "NULL" or mp_row[0][:2] == "OT" or \
                            mp_row[0][:1] == "P":
                if self.debug:
                    ind += 1
                continue

            next_opcodes = mp_row[10].split(';')  # how many next opcodes?
            if len(next_opcodes) > 1:  # if more then one, quantities will be derived from peg
                quant = None
            else:
                quant = int(mp_row[2].split('.')[0])  # else use quantity specified in a data

            # iterate over all next opcodes (even ir there is only on of it)
            for opcode in next_opcodes:
                if mp_row[0][0] == "W":
                    src = "DUMMY"
                elif mp_row[0][0] == "I":
                    src = "KESKLADU"
                else:
                    src = mp_row[8]
                data[(mp_row[0].strip(), opcode.strip())] = [src, None, mp_row[5], quant]

                # update mapper
                try:
                    mapper[opcode.strip()].append(mp_row[0].strip())
                except KeyError:
                    mapper[opcode] = [mp_row[0].strip()]

            if self.debug:
                ind += 1

        # stage 2: filling missed quantities parsing peg file
        for peg_row in self.peg_reader:
            try:
                data[peg_row[1], peg_row[2]][3] = int(peg_row[3].split('.')[0])
            except KeyError:
                pass

        if self.debug:
            count = 0

            for k, v in data.items():
                if v[3] is None or v[1] is None:
                    print("%s -> %s" % (str(k), str(v)))
                    count += 1

            print("---------------------\nTOTAL ERRORS FOUND IN DATA: %i" % count)
            print("---------------------\nTOTAL PARSED DATA ENTRIES: %i" % len(data))

    def __del__(self):
        """ Makes sure input files were were closed properly even on error """

        self.mp_f.close()
        self.peg_f.close()
