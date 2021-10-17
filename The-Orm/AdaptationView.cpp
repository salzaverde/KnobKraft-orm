/*
   Copyright (c) 2020 Christof Ruch. All rights reserved.

   Dual licensed: Distributed under Affero GPL license by default, an MIT license is available for purchase
*/

#include "AdaptationView.h"

#include "Capability.h"

#include "EditBufferCapability.h"
#include "ProgramDumpCapability.h"
#include "BankDumpCapability.h"
#include "DataFileLoadCapability.h"

#include "BundledAdaptation.h"

#include <boost/format.hpp>

namespace knobkraft {

	AdaptationView::AdaptationView() : extraFunctions_(900, LambdaButtonStrip::Direction::Horizontal)
	{
		addAndMakeVisible(adaptationInfo_);

		LambdaButtonStrip::TButtonMap buttons = {
			{ "ReloadAdaptation", { "Reload python file", [this]() {
				if (adaptation_ && adaptation_->isFromFile()) {
					adaptation_->reloadPython();
					setupForAdaptation(adaptation_);
				}
				else {
					AlertWindow::showMessageBox(AlertWindow::InfoIcon, "Not a user defined adaptation", "Only Adaptation modules that are loaded from a Python script can be reloaded");
				}
			}}},
			{ "EditAdaptation", { "Edit python file", [this]() {
				if (adaptation_) {
					if (!adaptation_->isFromFile()) {
						// Not possible yet, but offer to break out from binary
						if (AlertWindow::showOkCancelBox(AlertWindow::InfoIcon, "Not a user defined adaptation", "This adaptation is a built-in module. We can break it out into the file system so you can edit it\n\n"
							"Should you wish to go back to the built-in version, just delete the file that will be created!", "Break out", "Cancel")) {
							if (BundledAdaptations::breakOut(adaptation_->getName())) {
								AlertWindow::showMessageBox(AlertWindow::InfoIcon, "File created", "We created the file. Please restart the KnobKraft Orm and continue with the edit operation");
							}
						}
						return;
					}

					// Just reveal to user - launching python files with the URL command is useless, because it will probably just try to run the python script instead of opening an editor.
					File adaptationSource(adaptation_->getSourceFilePath());
					if (adaptationSource.exists()) {
							adaptationSource.revealToUser();
					}
				}
			}}}
		};

		extraFunctions_.setButtonDefinitions(buttons);
		addAndMakeVisible(extraFunctions_);
		addAndMakeVisible(setupHelp_);
		addAndMakeVisible(knobkraftWiki_);
	}

	void AdaptationView::setupForAdaptation(std::shared_ptr<GenericAdaptation> const& adaptationSynth)
	{
		adaptation_ = adaptationSynth;
		std::string infoText;
		infoText = (boost::format("Implementation information for the adaptation for the '%s':\n\n") % adaptationSynth->getName()).str();

		bool failure = false;
		for (auto functionName : kMinimalRequiredFunctionNames) {
			if (!adaptationSynth->pythonModuleHasFunction(functionName)) {
				infoText += (boost::format("Error: Required function %s has not been implemented yet\n") % functionName).str();
				failure = true;
			}
		}
		if (!failure) {
			infoText += "All required functions have been implemented\n";
		}
		infoText += "\n";

		auto hasEditBuffer = midikraft::Capability::hasCapability<midikraft::EditBufferCapability>(adaptationSynth);
		auto hasProgramDump = midikraft::Capability::hasCapability<midikraft::ProgramDumpCabability>(adaptationSynth);
		auto hasBankDump = midikraft::Capability::hasCapability<midikraft::BankDumpCapability>(adaptationSynth);
		auto hasDataFileLoad = midikraft::Capability::hasCapability<midikraft::DataFileLoadCapability>(adaptationSynth);

		infoText += (boost::format("Edit Buffer Capability has %sbeen implemented\n") % (hasEditBuffer ? "" : "not ")).str();
		infoText += (boost::format("Program Dump Capability has %sbeen implemented\n") % (hasProgramDump ? "" : "not ")).str();
		infoText += (boost::format("Bank Dump Capability has %sbeen implemented\n") % (hasBankDump ? "" : "not ")).str();
		infoText += (boost::format("Data File Load Capability has %sbeen implemented\n") % (hasDataFileLoad ? "" : "not ")).str();

		infoText += "\n\nImplemented functions:\n\n";
		for (auto functionName : kAdapatationPythonFunctionNames) {
			if (adaptationSynth->pythonModuleHasFunction(functionName)) {
				infoText += (boost::format("def %s()\n") % functionName).str();
			}
		}
		infoText += "\n\nNot implemented functions:\n\n";
		for (auto functionName : kAdapatationPythonFunctionNames) {
			if (!adaptationSynth->pythonModuleHasFunction(functionName)) {
				infoText += (boost::format("def %s()\n") % functionName).str();
			}
		}

		adaptationInfo_.setText(infoText, false);

		// Setup help
		
		setupHelp_.setText(adaptation_->setupHelpText(), false);
		knobkraftWiki_.setButtonText(adaptation_->getName() + " in the KnobKraft Wiki");
		String pageName = String(adaptation_->getName()).replace(" ", "-");
		knobkraftWiki_.setURL(URL("https://github.com/christofmuc/KnobKraft-orm/wiki/" + pageName));
	}

	void AdaptationView::resized()
	{
		auto area = getLocalBounds();

		extraFunctions_.setBounds(area.removeFromBottom(60).reduced(8));

		// Left column 
		FlexBox leftColumn;
		leftColumn.flexDirection = FlexBox::Direction::column;
		leftColumn.items.add(FlexItem(knobkraftWiki_).withHeight(30));
		leftColumn.items.add(FlexItem(setupHelp_).withFlex(1.0f).withMargin({ 8, 0, 0, 0 }));

		// Two column view
		FlexBox layout;
		layout.flexDirection = FlexBox::Direction::row;
		layout.alignContent = FlexBox::AlignContent::stretch;
		layout.justifyContent = FlexBox::JustifyContent::center;
		layout.items.add(FlexItem(leftColumn).withWidth(600).withMargin({ 0, 4, 0, 0 }));
		layout.items.add(FlexItem(adaptationInfo_).withWidth(600).withMargin({ 0, 0, 0, 4 }));
		layout.performLayout(area.reduced(8));
	}

}