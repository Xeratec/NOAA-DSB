# NOAA-DSB

### A student project for the P&S Software Defined Radio @ ETH Zurich
NOAA-DSB is a satellite receiver, demodulator and decoder for the [DSB](https://www.sigidwiki.com/wiki/NOAA_Direct_Sounder_Broadcast_(DSB)) signal of NOAA weather satellites.

#### Further Information is available here:

* **[Information Sheet]()**
* **[Presentation]()**

# The Team
**Philip Wiese** (ETHZ Bsc ETIT)  
*Antenna Design, Python* - [Xeratec](https://github.com/Xeratec)  

**Julian Merkhover** (ETHZ Bsc ETIT)  
*Python* - [julianmer](https://github.com/julianmer)

**Sevrin Mathys** (ETHZ Bsc ETIT)  
*GnuRadio, Python* - [SevyRide](https://github.com/SevyRide)

# Usage
Demodulate Raw I/Q audio from gqrx or similar programs
```sh
$ python2.7 src/demodulator/noaa_demodulate.py -f recordings/samples/POES_56k250.raw -r 56250
```

Extract TIP frames
```sh
$ python src/decoder/noaa_decode.py -f demod.raw -v 1
```

Decode TIP frames
```sh
TODO
```

### Dependencies
The project has the following dependencies, make sure you have them all installed:
- Python2.7
- Python3
- tqdm (Python3)
- gnuradio
- SciPy

# ToDo
* Telemetry Decoder
* Documentation

# Links for Developer
* [Live WebSDR vom NOAA Frequenzbereich](http://k3fef.com:8902)
* [About SEM-2](http://www.esa.int/Our_Activities/Observing_the_Earth/Meteorological_missions/MetOp/About_SEM-2)
* [NOAA / POES Space Environment Monitor](https://www.ngdc.noaa.gov/stp/satellite/poes/)

**Tutorials**
* [NOAA Weather Satellite Reception with GNU Radio and USRP](http://oz9aec.net/radios/gnu-radio/noaa-weather-satellite-reception-with-gnu-radio-and-usrp)
* [NOAA POES TIP Demodulation](http://wiki.nebarnix.com/wiki/NOAA_POES_TIP_Demodulation)
* [Decoding the NOAA Weather Satellite Telemetry Beacons](https://www.rtl-sdr.com/decoding-the-noaa-weather-satellite-telemetry-beacons/)
