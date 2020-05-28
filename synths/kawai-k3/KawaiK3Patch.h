/*
   Copyright (c) 2020 Christof Ruch. All rights reserved.

   Dual licensed: Distributed under Affero GPL license by default, an MIT license is available for purchase
*/

#pragma once

#include "Patch.h"
#include "DetailedParametersCapability.h"

#include "KawaiK3Parameter.h"
#include "PatchNumber.h"

#include "Additive.h"


namespace midikraft {

	class KawaiK3PatchNumber : public PatchNumber {
	public:
		using PatchNumber::PatchNumber;
		virtual std::string friendlyName() const;
	};

	class KawaiK3WaveNumber : public PatchNumber {
	public:
		using PatchNumber::PatchNumber;
		virtual std::string friendlyName() const;
	};

	class KawaiK3Wave : public Patch {
	public:
		KawaiK3Wave(Synth::PatchData const &data, MidiProgramNumber programNo);
		KawaiK3Wave(const Additive::Harmonics& harmonics, MidiProgramNumber programNo);

		std::string name() const override;

		std::shared_ptr<PatchNumber> patchNumber() const override;
		void setPatchNumber(MidiProgramNumber patchNumber) override;

	private:
		MidiProgramNumber programNo_;
	};

	class KawaiK3Patch : public Patch, public DetailedParametersCapability {
	public:
		KawaiK3Patch(MidiProgramNumber programNo, Synth::PatchData const &patchdata);

		static std::shared_ptr<KawaiK3Patch> createInitPatch();

		// Implementation of Patch interface
		virtual std::string name() const override;
		virtual std::shared_ptr<PatchNumber> patchNumber() const override;
		virtual void setPatchNumber(MidiProgramNumber patchNumber) override;

		int value(SynthParameterDefinition const &param) const;
		void setValue(KawaiK3Parameter const &param, int value);

		virtual std::vector<std::shared_ptr<SynthParameterDefinition>> allParameterDefinitions() const override;

		Additive::Harmonics harmonicsFromWave();

		bool needsUserWave() const;
		void addWaveIfOscillatorUsesIt(std::shared_ptr<DataFile> wave);

	private:
		KawaiK3PatchNumber number_;
	};

}