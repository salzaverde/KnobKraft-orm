/*
   Copyright (c) 2020 Christof Ruch. All rights reserved.

   Dual licensed: Distributed under Affero GPL license by default, an MIT license is available for purchase
*/

#pragma once

#include "Synth.h"

#include "MidiController.h"
#include "Patch.h"
#include "Additive.h"
#include "DrawbarOrgan.h"
#include "SupportedByBCR2000.h"

#include "ProgramDumpCapability.h"
#include "BankDumpCapability.h"
#include "ReadonlySoundExpander.h"
#include "AdditiveCapability.h"
#include "HybridWaveCapability.h"
#include "DataFileLoadCapability.h"
#include "DetailedParametersCapability.h"
#include "BidirectionalSyncCapability.h"
#include "SendsProgramChangeCapability.h"

#include "SupportedByBCR2000.h" // Should be moved into the bidirectional sync?

#include <set>

namespace midikraft {

	class KawaiK3Wave;
	class KawaiK3Parameter;
	class KawaiK3Control;
	class SynthView;

	class KawaiK3 : public Synth, public SupportedByBCR2000, public SimpleDiscoverableDevice, public ProgramDumpCabability, public BankDumpCapability,
		public DataFileLoadCapability, public DataFileSendCapability, public DetailedParametersCapability, public BidirectionalSyncCapability,
		public SendsProgramChangeCapability,
		public ReadonlySoundExpander, public AdditiveCapability, public HybridWaveCapability {
	public:
		static const MidiProgramNumber kFakeEditBuffer;

		enum DataFileType {
			K3_PATCH = 0,
			K3_WAVE = 1
		};

		enum class WaveType {
			USER_WAVE = 100,
			USER_WAVE_CARTRIDGE = 101,
			//MIDI_WAVE = 102// This is peculiar, I still have to find out what that is? Might be mistaken in the manual, because my K3M does not respond to code 102
		};

		KawaiK3();

		// Basic Synth implementation
		virtual std::string getName() const override;
		virtual bool isOwnSysex(MidiMessage const &message) const override;
		virtual int numberOfBanks() const override;
		virtual int numberOfPatches() const override;
		virtual std::string friendlyBankName(MidiBankNumber bankNo) const override;

		std::shared_ptr<DataFile> patchFromPatchData(const Synth::PatchData &data, MidiProgramNumber place) const override;

		// Special Synth implementation
		virtual void sendPatchToSynth(MidiController *controller, SimpleLogger *logger, std::shared_ptr<DataFile> dataFile) override;

		// Discoverable Device
		virtual std::vector<juce::MidiMessage> deviceDetect(int channel) override;
		virtual int deviceDetectSleepMS() override;
		virtual MidiChannel channelIfValidDeviceResponse(const MidiMessage &message) override;
		virtual bool needsChannelSpecificDetection() override;

		juce::MidiMessage createSetParameterMessage(KawaiK3Parameter *param, int paramValue);
		void determineParameterChangeFromSysex(juce::MidiMessage const &message, KawaiK3Parameter **param, int *paramValue);
		juce::MidiMessage mapCCtoSysex(juce::MidiMessage const &ccMessage);

		// Program Dump Capability
		virtual std::vector<MidiMessage> requestPatch(int patchNo) const override;
		virtual bool isSingleProgramDump(const MidiMessage& message) const override;
		virtual std::shared_ptr<Patch> patchFromProgramDumpSysex(const MidiMessage& message) const override;
		virtual std::vector<MidiMessage> patchToProgramDumpSysex(const Patch &patch) const override;
		virtual TPatchVector patchesFromSysexBank(const MidiMessage& message) const override;

		// Bank Dump Capability
		virtual std::vector<MidiMessage> requestBankDump(MidiBankNumber bankNo) const override;
		virtual bool isBankDump(const MidiMessage& message) const override;
		virtual bool isBankDumpFinished(std::vector<MidiMessage> const &bankDump) const override;

		// SoundExpanderCapability
		virtual MidiChannel getInputChannel() const override;

		// AdditiveCapability
		virtual void selectRegistration(Patch *currentPatch, DrawbarOrgan::RegistrationDefinition selectedRegistration) override;
		virtual void selectHarmonics(Patch *currentPatch, std::string const &name, Additive::Harmonics const &selectedHarmonics) override;

		// HybridWaveCapability
		virtual std::vector<float> romWave(int waveNo) override;
		virtual std::string waveName(int waveNo) override;

		// Implementation of BCR2000 sync
		virtual std::vector<std::string> presetNames() override;
		virtual void setupBCR2000(BCR2000 &bcr) override;
		virtual void syncDumpToBCR(MidiProgramNumber programNumber, BCR2000 &bcr) override;
		virtual void setupBCR2000View(BCR2000Proxy* view, TypedNamedValueSet& parameterModel, ValueTree& valueTree) override;

		// This needs to be overridden to handle the wave dumps together with the patch dumps
		virtual TPatchVector loadSysex(std::vector<MidiMessage> const &sysexMessages) override;

		// Kawai K3 specifics
		std::shared_ptr<Patch> patchFromSysex(const MidiMessage& message, MidiProgramNumber programIndex) const;
		MidiMessage patchToSysex(Synth::PatchData const &patch, int programNo, bool produceWaveInsteadOfPatch) const;

		void retrieveWave();
		void sendK3Wave(Patch *patch, MidiMessage const &userWave);

		// Kawai K3 specifics
		typedef std::vector<uint8> WaveData;

		MidiMessage requestWaveBufferDump(WaveType waveType) const;
		bool isWaveBufferDump(const MidiMessage& message) const;
		bool isBankDumpAndNotWaveDump(const MidiMessage& message) const;
		std::shared_ptr<DataFile> waveFromSysex(const MidiMessage& message) const;
		MidiMessage waveToSysex(std::shared_ptr<KawaiK3Wave> wave);

		bool isWriteConfirmation(MidiMessage const &message);

		// DataFileLoadCapability
		virtual std::vector<MidiMessage> requestDataItem(int itemNo, int dataTypeID) override;
		virtual int numberOfDataItemsPerType(int dataTypeID) const override;
		virtual bool isDataFile(const MidiMessage &message, int dataTypeID) const override;
		virtual std::vector<std::shared_ptr<DataFile>> loadData(std::vector<MidiMessage> messages, int dataTypeID) const override;
		virtual std::vector<DataFileDescription> dataTypeNames() const override;

		// DataFileSendCapability
		virtual std::vector<MidiMessage> dataFileToMessages(std::shared_ptr<DataFile> dataFile) const override;

		// DetailedParametersCapability
		std::vector<std::shared_ptr<SynthParameterDefinition>> allParameterDefinitions() const override;

		// BidirectionalSyncCapability
		virtual bool determineParameterChangeFromSysex(std::vector<juce::MidiMessage> const& messages, SynthParameterDefinition **outParam, int &outValue) override;

		// SendsProgramChangeCapability
		void gotProgramChange(MidiProgramNumber newNumber) override;
		MidiProgramNumber lastProgramChange() const override;

	private:
		friend class KawaiK3Control;
		friend class KawaiK3Parameter;

		// See Manual p. 49 for the sysex "commands"
		enum SysexFunction {
			ONE_BLOCK_DATA_REQUEST = 0,
			ALL_BLOCK_DATA_REQUEST = 1,
			PARAMETER_SEND = 16,
			ONE_BLOCK_DATA_DUMP = 32,
			ALL_BLOCK_DATA_DUMP = 33,
			WRITE_COMPLETE = 64,
			WRITE_ERROR = 65,
			WRITE_ERROR_BY_PROTECT = 66,
			WRITE_ERROR_BY_NO_CARTRIDGE = 67,
			MACHINE_ID_REQUEST = 96,
			MACHINE_ID_ACKNOWLEDE = 97,
			INVALID_FUNCTION = 255
		};
		static const std::set<SysexFunction> validSysexFunctions;

		std::vector<uint8> buildSysexFunction(SysexFunction function, uint8 subcommand) const;
		juce::MidiMessage buildSysexFunctionMessage(SysexFunction function, uint8 subcommand) const;
		SysexFunction sysexFunction(juce::MidiMessage const &message) const;
		uint8 sysexSubcommand(juce::MidiMessage const &message) const;

		MidiController::HandlerHandle k3BCRSyncHandler_ = MidiController::makeNoneHandle();

		MidiProgramNumber programNo_;
	};

}