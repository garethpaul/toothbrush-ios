//
//  Hex.swift
//

import Foundation
import UIKit

// Converts a hex string into a UIColor.
func toColor(_ hex: String) -> UIColor {
    var cString = hex.trimmingCharacters(in: .whitespacesAndNewlines).uppercased()

    if cString.hasPrefix("#") {
        cString.removeFirst()
    }

    if cString.count != 6 {
        return UIColor.gray
    }

    var rgbValue: UInt64 = 0
    let scanner = Scanner(string: cString)
    if !scanner.scanHexInt64(&rgbValue) || !scanner.isAtEnd {
        return UIColor.gray
    }

    return UIColor(
        red: CGFloat((rgbValue & 0xFF0000) >> 16) / 255.0,
        green: CGFloat((rgbValue & 0x00FF00) >> 8) / 255.0,
        blue: CGFloat(rgbValue & 0x0000FF) / 255.0,
        alpha: CGFloat(1.0)
    )
}
