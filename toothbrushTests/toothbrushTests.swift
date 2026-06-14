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
}
