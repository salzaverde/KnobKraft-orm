/*
   Copyright (c) 2020 Christof Ruch. All rights reserved.

   Dual licensed: Distributed under Affero GPL license by default, an MIT license is available for purchase
*/

#pragma once


#include "ProgramDumpCapability.h"

#include "GenericAdaptation.h"

namespace knobkraft {

	class GenericProgramDumpCapability : public midikraft::ProgramDumpCabability {
	public:
		GenericProgramDumpCapability(GenericAdaptation *me) : me_(me) {}
		virtual std::vector<MidiMessage> requestPatch(int patchNo) const override;
		virtual bool isSingleProgramDump(const MidiMessage& message) const override;
		virtual std::shared_ptr<midikraft::Patch> patchFromProgramDumpSysex(const MidiMessage& message) const override;
		virtual std::vector<MidiMessage> patchToProgramDumpSysex(const midikraft::Patch &patch) const override;

	private:
		GenericAdaptation *me_;
	};

}
