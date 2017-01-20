from math import sqrt
import csv

class FlightCalculator():
    def __init__(self, **kwargs):
        self.V = float(kwargs["V"])
        self.hfp = float(kwargs["hfp"])
        self.hmax = float(kwargs["hmax"])
        self.hmin = float(kwargs["hmin"])
        self.hltn = float(kwargs["hltn"])
        self.M = float(kwargs["M"])
        self.ck = float(kwargs["ck"])
        self.ce = float(kwargs["ce"])
        self.lzd = float(kwargs["lzd"])
        self.a = float(kwargs["a"])
        self.b = float(kwargs["b"])
        self.pa = float(kwargs["pa"])
        self.pb = float(kwargs["pb"])
        self.pixelS = float(kwargs["pixelS"])
        self.Ly = float(kwargs["Ly"])
        self.Lx = float(kwargs["Lx"])
        self.p = float(kwargs["p"])
        self.q = float(kwargs["q"])

    def wymTerPop(self):
        self.y = ((self.hfp - self.ck) / self.ck) * self.a/1000
        return self.y

    def wymTerPod(self):
        self.x = (self.hfp - self.ck) / self.ck * self.b/1000
        return self.x

    def czasWykZdj(self):
        self.ct = 60 / self.lzd
        return self.ct

    def dystansMiedzyZdj(self):
        self.s = self.V * self.czasWykZdj()
        return self.s

    def mianSklZdj(self):
        self.mz = self.hfp / self.ck
        return self.mz

    def wspEmpirC(self):
        self.c = self.mz / sqrt(self.M)
        return self.c

    def wysSrednia(self):
        self.hsr = (self.hmax + self.hmin) / 2
        return self.hsr

    def wysFoto(self):
        self.hf = self.ck * self.mz
        return self.hf

    def wysLotuWzLotniskaSrednia(self):
        self.hwzg_ltn = self.hf + self.hsr - self.hltn
        return self.hwzg_ltn

    def sklZdj(self):
        return self.ck / self.hf

    def terWymPix(self):
        self.GSD = self.pixelS * self.hf / self.ck
        return self.GSD

    def terWymPixMin(self):
        self.GSD = self.pixelS * (self.hf -( self.hmax - self.hsr)) / self.ck
        return self.GSD

    def terWymPixMax(self):
        self.GSD = self.pixelS * (self.hf + self.hsr - self.hmin) / self.ck
        return self.GSD

    def powArkMapy(self):
        self.Po = self.Lx * self.Ly
        return self.Po

    def bazaPod(self):
        self.Bp = self.wymTerPod() * (100 - self.p) / 100
        return self.Bp

    def bazaPop(self):
        self.Bq = self.wymTerPop() * (100 - self.q) / 100
        return self.Bq

    def liczbaSzereg(self):
        self.Ny = self.Ly / self.bazaPop() + 1.0
        return self.Ny

    def liczbaZdjSzereg(self):
        self.Nx = self.Lx / self.Bp + 5
        return self.Nx

    def liczbaZdjTotal(self):
        self.Ntotal = self.liczbaSzereg() * self.liczbaZdjSzereg()
        return self.Ntotal

    def dlgSzereg(self):
        self.Dp = self.bazaPod() * self.liczbaZdjSzereg()/1000
        return self.Dp

    def terZasiegZdjX(self):
        self.Lzx = self.b * self.mianSklZdj()/1000
        return self.Lzx

    def terZasiegZdjY(self):
        self.Lzy = self.a * self.mianSklZdj()/1000
        return self.Lzy

    def powZdj(self):
        self.Pz = self.terZasiegZdjX() * self.terZasiegZdjY()
        return self.Pz

    def powStereogram(self):
        self.Pm = (self.terZasiegZdjX() - self.bazaPop()) * self.terZasiegZdjY()
        return self.Pm

    def powUzStereogram(self):
        self.Pn = self.bazaPop() * self.bazaPod()
        return self.Pn

    def dlgNalotu(self):
        self.D = self.liczbaSzereg() * self.Lx + self.Ly
        return self.D

    def czasLotu(self):
        self.t_tot = self.dlgNalotu() / self.V/60
        return self.t_tot

    def wlkRozmazania(self):
        self.ds = self.V * self.ce / self.mianSklZdj() * 1000
        return self.ds

    def czasOtwMigawki(self):
        self.tm = self.wlkRozmazania() * self.mianSklZdj() / self.V/1000
        return self.tm

    def calculateAll(self):
        self.results =dict()
        self.results["Wymiar_Ternowy_Podlurzny"]=             self.wymTerPod()
        self.results["Wymiar Terenowy Poprzeczny"] =          self.wymTerPop()
        self.results["Czas Wykonywania Zdjecia"] =            self.czasWykZdj()
        self.results["Dystans Miedzy Zdjeciami"] =            self.dystansMiedzyZdj()
        self.results["Mianownik Skali Zdjecia"] =             self.mianSklZdj()
        self.results["Wspolczynnik Empiryczny c"]=            self.wspEmpirC()
        self.results["Wysokosc Srednia"] =                    self.wysSrednia()
        self.results["Wysokosc Fotografowania"]=              self.wysFoto()
        self.results["Wysokosc Wzgledem Lotniska"]=           self.wysLotuWzLotniskaSrednia()
        self.results["Skala Zdjecia"]=                        self.sklZdj()
        self.results["Teremowy Wymiar Piksela"]=              self.terWymPix()
        self.results["Terenowy Wymiar Piksela - Minimalny"]=  self.terWymPixMin()
        self.results["Terenowy Wymiar Piksela - Maksymalny"]= self.terWymPixMax()
        self.results["Powierzchnia Arkusza Mapy"]=            self.powArkMapy()
        self.results["Baza Podluzna"]=                        self.bazaPod()
        self.results["Baza Poprzeczna"]=                      self.bazaPop()
        self.results["Liczba Szeregow"]=                      self.liczbaSzereg()
        self.results["Liczba Zdjec w Szeregu"]=               self.liczbaZdjSzereg()
        self.results["Liczba Zdjec Calkowita"]=               self.liczbaZdjTotal()
        self.results["Dlugosc Szeregu"]=                      self.dlgSzereg()
        self.results["Terenowy Zasieg Zdjecia - X"]=          self.terZasiegZdjX()
        self.results["Terenowy Zasieg Zdjecia - Y"]=          self.terZasiegZdjY()
        self.results["Powierzchnia Zdjecia"]=                 self.powZdj()
        self.results["Powierzchnia Stereogramu"]=             self.powStereogram()
        self.results["Powierzchnia Uzyteczna Stereogramu"]=   self.powUzStereogram()
        self.results["Dlugosc Nalotu"]=                       self.dlgNalotu()
        self.results["Czas Lotu"]=                            self.czasLotu()
        self.results["Wielkosc Rozmazania"]=                  self.wlkRozmazania()
        self.results["Czas Otwarcia Migawki"]=                self.czasOtwMigawki()

    def saveResInFile(self,filename):
        with open(filename,'w') as f:
            w = csv.writer(f)
            w.writerows(self.results.items())

    def calculateVariable(self,save, **variable):
        varName = variable.keys()
        varValues = variable[varName[0]]
        varResults = []
        for varValue in varValues:
            self.__dict__[varName[0]] = varValue
            S.calculateAll()
            varResults.append(S.results.items())
        varOrderedResults = []

        varNames = []
        for varnum in range(len(varResults[0])):
            varOrdered = []
            for res in varResults:
                varOrdered.append(res[varnum][1])
            varNames.append(res[varnum][0])
            varOrderedResults.append(varOrdered)
        varOrderedNamedResults = []
        for name,varVal in zip(varNames,varOrderedResults):
            varOrderedNamedResults.append([name,varVal])
        if save:
            self.saveVarResults(varOrderedNamedResults,"analiza_parametru_" + varName[0] + ".csv")

    def saveVarResults(self,varList,filename):
        with open(filename,'w') as f:
            w = csv.writer(f)
            w.writerows(varList)





        #self.
        #for value in variable:

if __name__ == "__main__":
    hmax = 269
    hmin = 239
    hltn = 124
    ht_sr = (hmax + hmin) / 2
    h=[125,150,175,200,225,250,275,300,325,350,375,400,425,450,475,500]
    V=[10,12,14,16,18,20,22]
    ck=[20e-3,30e-3,40e-3,50e-3,60e-3,70e-3,80e-3]

    #for height in h:
    S = FlightCalculator(V=22, hfp=h[1], hmin=hmin, hmax=hmax, hltn=hltn, M=2000,
                         ck=80e-3, ce=0.002, a=36.7, b=49.1, pa=6132, pb=8176,
                         pixelS=6e-6, Ly=4000, Lx=4000, p=60, q=25, lzd=50)

    S.calculateVariable(True,hfp=h)
    S.calculateAll()
    S.saveResInFile("wynik_wysokosc_class" + str(h[1]) + ".txt")
    print(S.results.items())
    f = open("wynik_wysokosc_" + str(h[1]) + ".txt", 'w')
    f.write("Wymiar Ternowy Podlurzny: " + str(S.wymTerPod()) + "\n")
    f.write("Wymiar Terenowy Poprzeczny: " + str(S.wymTerPop()) + "\n")
    f.write("Czas Wykonywania Zdjecia: " + str(S.czasWykZdj()) + "\n")
    f.write("Dystans Miedzy Zdjeciami: " + str(S.dystansMiedzyZdj()) + "\n")
    f.write("Mianownik Skali Zdjecia: " + str(S.mianSklZdj()) + "\n")
    f.write("Wspolczynnik Empiryczny c: " + str(S.wspEmpirC()) + "\n")
    f.write("Wysokosc Srednia: " + str(S.wysSrednia()) + "\n")
    f.write("Wysokosc Fotografowania: " + str(S.wysFoto()) + "\n")
    f.write("Wysokosc Wzgledem Lotniska: " + str(S.wysLotuWzLotniskaSrednia()) + "\n")
    f.write("Skala Zdjecia: " + str(S.sklZdj()) + "\n")
    f.write("Teremowy Wymiar Piksela: " + str(S.terWymPix()) + "\n")
    f.write("Terenowy Wymiar Piksela - Minimalny: " + str(S.terWymPixMin()) + "\n")
    f.write("Terenowy Wymiar Piksela - Maksymalny: " + str(S.terWymPixMax()) + "\n")
    f.write("Powierzchnia Arkusza Mapy: " + str(S.powArkMapy()) + "\n")
    f.write("Baza Podluzna: " + str(S.bazaPod()) + "\n")
    f.write("Baza Poprzeczna: " + str(S.bazaPop()) + "\n")
    f.write("Liczba Szeregow: " + str(S.liczbaSzereg()) + "\n")
    f.write("Liczba Zdjec w Szeregu: " + str(S.liczbaZdjSzereg()) + "\n")
    f.write("Liczba Zdjec Calkowita: " + str(S.liczbaZdjTotal()) + "\n")
    f.write("Dlugosc Szeregu: " + str(S.dlgSzereg()) + "\n")
    f.write("Terenowy Zasieg Zdjecia - X: " + str(S.terZasiegZdjX()) + "\n")
    f.write("Terenowy Zasieg Zdjecia - Y: " + str(S.terZasiegZdjY()) + "\n")
    f.write("Powierzchnia Zdjecia: " + str(S.powZdj()) + "\n")
    f.write("Powierzchnia Stereogramu: " + str(S.powStereogram()) + "\n")
    f.write("Powierzchnia Uzyteczna Stereogramu: " + str(S.powUzStereogram()) + "\n")
    f.write("Dlugosc Nalotu: " + str(S.dlgNalotu()) + "\n")
    f.write("Czas Lotu: " + str(S.czasLotu()) + "\n")
    f.write("Wielkosc Rozmazania: " + str(S.wlkRozmazania()) + "\n")
    f.write("Czas Otwarcia Migawki: " + str(S.czasOtwMigawki()) + "\n")
    f.close()
