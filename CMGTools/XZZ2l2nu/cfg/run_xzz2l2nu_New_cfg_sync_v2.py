##########################################################
##      configuration for XZZ2l2nu 
##########################################################

import CMGTools.XZZ2l2nu.fwlite.Config as cfg
from CMGTools.XZZ2l2nu.fwlite.Config import printComps
from CMGTools.XZZ2l2nu.RootTools import *
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

syncChannel="Muon"
#syncChannel="Electron"

#Load all common analyzers
from CMGTools.XZZ2l2nu.analyzers.coreXZZ_cff import *

#-------- SAMPLES AND TRIGGERS -----------
from CMGTools.XZZ2l2nu.samples.loadSamples import *
selectedComponents = mcSamples+dataSamples

triggerFlagsAna.triggerBits ={
    "ISOMU":triggers_1mu_iso,
    "MU":triggers_1mu_noniso,
    "ISOELE":triggers_1e,
    "ELE":triggers_1e_noniso,
    "HT800":triggers_HT800,
    "HT900":triggers_HT900,
    "JJ":triggers_dijet_fat,
    "MET90":triggers_met90_mht90+triggers_metNoMu90_mhtNoMu90,
    "MET120":triggers_metNoMu120_mhtNoMu120
}

if syncChannel == "Muon":
    genAna.filter = "ZZ2mu"
    for comp in mcSamples+otherMcSamples:
        comp.triggers=triggers_1mu_noniso

if syncChannel == "Electron":
    genAna.filter = "ZZ2el"
    for comp in mcSamples+otherMcSamples:
        comp.triggers=triggers_1e_noniso 

leptonicVAna.selectMuMuPair = (lambda x: (x.leg1.highPtID or x.leg2.highPtID) and ((x.leg1.pt()>50.0 and abs(x.leg1.eta())<2.1) or (x.leg2.pt()>50.0 and abs(x.leg2.eta())<2.1)))
leptonicVAna.selectElElPair = (lambda x: x.leg1.pt()>115.0 or x.leg2.pt()>115.0 )
leptonicVAna.selectVBoson = (lambda x: x.pt()>200.0 and x.mass()>70.0 and x.mass()<110.0)

#-------- Analyzer
from CMGTools.XZZ2l2nu.analyzers.treeXZZ_cff import *

vvTreeProducer.globalVariables = [
         NTupleVariable("nVert",  lambda ev: len(ev.goodVertices), int, help="Number of good vertices"),
         ]
vvTreeProducer.globalObjects =  { }
vvTreeProducer.collections = {
         "LL"  : NTupleCollection("Zll",LLType,5, help="Z to ll"),
         "selectedLeptons" : NTupleCollection("lep",leptonType,10, help="selected leptons"),
         "genLeptons" : NTupleCollection("genLep", genParticleType, 10, help="Generated leptons (e/mu) from W/Z decays"),
         "genZBosons" : NTupleCollection("genZ", genParticleType, 10, help="Generated V bosons"),
     }



#-------- SEQUENCE
#sequence = cfg.Sequence(coreSequence+[vvSkimmer,vvTreeProducer])

coreSequence = [
    skimAnalyzer,
    genAna,
    triggerAna,
    vertexAna,
    lepAna,
    leptonicVAna,
    dumpEvents,
]
    
#sequence = cfg.Sequence(coreSequence)
sequence = cfg.Sequence(coreSequence+[vvTreeProducer])

 

#-------- HOW TO RUN
test = 1
if test==1:
    # test a single component, using a single thread.
    #selectedComponents = dataSamples
    #selectedComponents = [SingleMuon_Run2015D_Promptv4,SingleElectron_Run2015D_Promptv4]
    #[SingleElectron_Run2015D_Promptv4,SingleElectron_Run2015D_05Oct]
    #selectedComponents = [RSGravToZZToZZinv_narrow_800]
    #selectedComponents = [BulkGravToZZ_narrow_800]
    selectedComponents = bulkJetsSamples
    #if syncChannel=="Muon":
    #    selectedComponents = [BulkGravToZZToZlepZhad_narrow_2000,BulkGravToZZToZlepZhad_narrow_3500,BulkGravToZZToZlepZhad_narrow_4500]
    #else:
        #selectedComponents = [BulkGravToZZToZlepZhad_narrow_1000,BulkGravToZZToZlepZhad_narrow_1200,BulkGravToZZToZlepZhad_narrow_2500]
    #    selectedComponents = bulkJetsSamples
    for c in selectedComponents:
        c.splitFactor = 1
        #c.triggers=triggers_1mu_noniso
        #c.triggers=triggers_1e_noniso
        #c.files = c.files[0]

## output histogram
outputService=[]
from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
output_service = cfg.Service(
    TFileService,
    'outputfile',
    name="outputfile",
    fname='vvTreeProducer/tree.root',
    option='recreate'
    )
outputService.append(output_service)

from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
from CMGTools.TTHAnalysis.tools.EOSEventsWithDownload import EOSEventsWithDownload
event_class = EOSEventsWithDownload
event_class = Events
if getHeppyOption("nofetch"):
    event_class = Events
config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = [],
                     events_class = event_class)




