//
//  toothbrushTests.swift
//  toothbrushTests
//
//  Created by Gareth on 5/23/15.
//  Copyright (c) 2015 GarethPaul. All rights reserved.
//

import UIKit
import XCTest
@testable import toothbrush

final class ToothbrushTests: XCTestCase {
    func testHexColorParsesTrimmedHashValue() {
        let color = toColor("  #EA0796\n")
        var red: CGFloat = 0
        var green: CGFloat = 0
        var blue: CGFloat = 0
        var alpha: CGFloat = 0

        XCTAssertTrue(color.getRed(&red, green: &green, blue: &blue, alpha: &alpha))
        XCTAssertEqual(red, 234.0 / 255.0, accuracy: 0.001)
        XCTAssertEqual(green, 7.0 / 255.0, accuracy: 0.001)
        XCTAssertEqual(blue, 150.0 / 255.0, accuracy: 0.001)
        XCTAssertEqual(alpha, 1.0, accuracy: 0.001)
    }

    func testHexColorRejectsPartialInput() {
        XCTAssertEqual(toColor("EA0796suffix"), UIColor.gray)
    }

    func testRemainingSecondsUsesMonotonicDeadlineInsteadOfTickCount() {
        let start: TimeInterval = 1_000
        let deadline = start + 120

        XCTAssertEqual(remainingWholeSeconds(until: deadline, now: start), 120)
        XCTAssertEqual(
            remainingWholeSeconds(until: deadline, now: start + 1.1),
            119
        )
        XCTAssertEqual(
            remainingWholeSeconds(until: deadline, now: start + 120.1),
            0
        )
    }

    func testRemainingSecondsClampsIntervalsLargerThanIntMax() {
        XCTAssertEqual(
            remainingWholeSeconds(until: Double(Int.max), now: 0),
            Int.max
        )
    }

    func testRemainingSecondsTreatsInvalidClockValuesAsCompleted() {
        XCTAssertEqual(remainingWholeSeconds(until: .infinity, now: 0), 0)
        XCTAssertEqual(remainingWholeSeconds(until: 120, now: .nan), 0)
    }

    func testCountdownStateMakesCompletionImmediatelyTestable() {
        let start: TimeInterval = 1_000
        let deadline = start + 120

        XCTAssertEqual(
            countdownState(until: deadline, now: start),
            .running(seconds: 120)
        )
        XCTAssertEqual(
            countdownState(until: deadline, now: deadline - 0.1),
            .running(seconds: 1)
        )
        XCTAssertEqual(
            countdownState(until: deadline, now: deadline),
            .completed
        )
        XCTAssertEqual(
            countdownState(until: deadline, now: deadline + 1),
            .completed
        )
    }

    func testCountdownLabelUsesSingularAndPluralGrammar() {
        XCTAssertEqual(countdownLabelText(for: 0), "0 seconds")
        XCTAssertEqual(countdownLabelText(for: 1), "1 second")
        XCTAssertEqual(countdownLabelText(for: 120), "120 seconds")
    }

    @MainActor
    func testCountdownLabelKeepsVisibleAndAccessibilityTextInSync() {
        let controller = makeController()
        controller.second = 1

        controller.updateTimerLabel()

        XCTAssertEqual(controller.seconds.text, "1 second")
        XCTAssertEqual(controller.seconds.accessibilityValue, "1 second")
    }

    @MainActor
    func testCompletedCountdownResetsOnlyOnce() {
        let controller = makeController()
        controller.timerEndTime = 0

        controller.subtractTime()
        controller.subtractTime()

        XCTAssertEqual(controller.resetCount, 1)
    }

    @MainActor
    func testCancelledCountdownIgnoresItsStaleTimerGeneration() {
        let controller = makeController()
        controller.setupTimer()
        let cancelledGeneration = controller.timerGeneration

        controller.stopTimerAndResetPrompt()
        controller.timerDidFire(generation: cancelledGeneration, now: 0)

        XCTAssertEqual(controller.resetCount, 1)
        XCTAssertNil(controller.timerEndTime)
        XCTAssertEqual(controller.second, 0)
    }

    @MainActor
    func testRestartedCountdownIgnoresPreviousTimerGeneration() {
        let controller = makeController()
        controller.setupTimer()
        let previousGeneration = controller.timerGeneration
        controller.setupTimer()
        let currentGeneration = controller.timerGeneration
        controller.timerEndTime = 1_120
        controller.second = 120

        controller.timerDidFire(generation: previousGeneration, now: 1_100)
        XCTAssertEqual(controller.second, 120)

        controller.timerDidFire(generation: currentGeneration, now: 1_100)
        XCTAssertEqual(controller.second, 20)
    }

    @MainActor
    func testRestartInvalidatesPreviousTimer() {
        let controller = makeController()
        controller.setupTimer()
        let previousTimer = controller.timer

        controller.setupTimer()

        XCTAssertFalse(previousTimer?.isValid ?? true)
        XCTAssertTrue(controller.timer?.isValid ?? false)
        controller.stopTimerAndResetPrompt()
    }

    @MainActor
    func testStartAndStopKeepPromptVisibilityDeterministic() {
        let controller = makeController()

        controller.start(controller)
        XCTAssertTrue(controller.brushBtn.isHidden)
        XCTAssertFalse(controller.brushText.isHidden)
        XCTAssertEqual(controller.seconds.text, "120 seconds")

        controller.stopTimerAndResetPrompt()
        XCTAssertFalse(controller.brushBtn.isHidden)
        XCTAssertTrue(controller.brushText.isHidden)
        XCTAssertEqual(controller.seconds.text, "0 seconds")
        XCTAssertEqual(controller.seconds.accessibilityValue, "0 seconds")
    }

    @MainActor
    func testActivationReconciliationCompletesOnlyOnce() {
        let controller = makeController()
        controller.timerEndTime = 0

        controller.applicationDidBecomeActive(
            Notification(name: UIApplication.didBecomeActiveNotification)
        )
        controller.applicationDidBecomeActive(
            Notification(name: UIApplication.didBecomeActiveNotification)
        )

        XCTAssertEqual(controller.resetCount, 1)
        XCTAssertNil(controller.timerEndTime)
    }

    @MainActor
    func testRepeatingTimerDoesNotRetainDepartedController() {
        weak var weakController: ResetCountingViewController?

        autoreleasepool {
            var controller: ResetCountingViewController? = makeController()
            controller?.setupTimer()
            weakController = controller
            controller = nil
        }

        XCTAssertNil(weakController)
    }

    @MainActor
    private func makeController() -> ResetCountingViewController {
        let controller = ResetCountingViewController()
        controller.retainedSeconds = UILabel()
        controller.retainedBrushButton = UIButton()
        controller.retainedBrushText = UILabel()
        controller.seconds = controller.retainedSeconds
        controller.brushBtn = controller.retainedBrushButton
        controller.brushText = controller.retainedBrushText
        return controller
    }
}

private final class ResetCountingViewController: ViewController {
    private(set) var resetCount = 0
    var retainedSeconds: UILabel?
    var retainedBrushButton: UIButton?
    var retainedBrushText: UILabel?

    override func stopTimerAndResetPrompt() {
        resetCount += 1
        super.stopTimerAndResetPrompt()
    }
}
