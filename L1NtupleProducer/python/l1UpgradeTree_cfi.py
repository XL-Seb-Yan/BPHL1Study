import FWCore.ParameterSet.Config as cms

l1UpgradeTree = cms.EDAnalyzer(
    "L1UpgradeTreeProducer",
    egToken = cms.untracked.InputTag("gtStage2Digis","EGamma"),
    tauTokens = cms.untracked.VInputTag(cms.InputTag("caloStage2Digis","Tau")),
    jetToken = cms.untracked.InputTag("caloStage2Digis","Jet"),
    muonToken = cms.untracked.InputTag("gtStage2Digis","Muon"),
    muonLegacyToken = cms.untracked.InputTag("muonLegacyInStage2FormatDigis","legacyMuon"),
    sumToken = cms.untracked.InputTag("caloStage2Digis","EtSum"),
    maxL1Upgrade = cms.uint32(60)
)
