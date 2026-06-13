//
//  ViewController.swift
//  toothbrush
//
//  Created by Gareth on 5/23/15.
//  Copyright (c) 2015 GarethPaul. All rights reserved.
//

import Darwin
import UIKit

private let continuousTimebase: mach_timebase_info_data_t = {
    var info = mach_timebase_info_data_t()
    mach_timebase_info(&info)
    return info
}()

func continuousTime() -> TimeInterval {
    let ticks = Double(mach_continuous_time())
    let nanoseconds = ticks * Double(continuousTimebase.numer) / Double(continuousTimebase.denom)
    return nanoseconds / 1_000_000_000
}

func remainingWholeSeconds(
    until endTime: TimeInterval,
    now: TimeInterval = continuousTime()
) -> Int {
    max(0, Int(ceil(endTime - now)))
}

class ViewController: UIViewController {

    @IBAction func start(_ sender: Any) {
        setupTimer()
        brushBtn.isHidden = true
        brushText.isHidden = false
    }

    @IBOutlet weak var seconds: UILabel!
    @IBOutlet weak var brushBtn: UIButton!
    @IBOutlet weak var brushText: UILabel!

    var timer: Timer?
    var second = 0
    var count = 0
    var logoView: UIImageView?
    var timerEndTime: TimeInterval?

    deinit {
        NotificationCenter.default.removeObserver(
            self,
            name: UIApplication.didBecomeActiveNotification,
            object: nil
        )
        timer?.invalidate()
        removeNavigationLogo()
    }

    override func viewDidLoad() {
        super.viewDidLoad()

        logoView = UIImageView(frame: CGRect(x: 0, y: 0, width: 40, height: 40))
        logoView?.image = UIImage(named: "logo")?.withRenderingMode(.alwaysTemplate)
        logoView?.tintColor = toColor("#EA0796")
        updateNavigationLogoFrame()

        navigationController?.navigationBar.barTintColor = toColor("#F6EC28")

        showNavigationLogo()
        setupAccessibility()
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(applicationDidBecomeActive(_:)),
            name: UIApplication.didBecomeActiveNotification,
            object: nil
        )
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        showNavigationLogo()
    }

    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()
        updateNavigationLogoFrame()
    }

    func setupTimer() {
        timer?.invalidate()
        second = 120
        count = 0
        timerEndTime = continuousTime() + TimeInterval(second)

        updateTimerLabel()

        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            self?.subtractTime()
        }
        timer?.tolerance = 0.1
        if let timer = timer {
            RunLoop.main.add(timer, forMode: .common)
        }
        brushText.layer.removeAllAnimations()
        brushText.alpha = 0
        UIView.animate(withDuration: 0.5, delay: 0.5, options: [.repeat, .autoreverse], animations: {
            self.brushText.alpha = 1
        }, completion: nil)
    }

    @objc func subtractTime() {
        if let timerEndTime = timerEndTime {
            second = remainingWholeSeconds(until: timerEndTime)
        } else {
            second = 0
        }

        if second <= 0 {
            stopTimerAndResetPrompt()
            return
        }

        updateTimerLabel()
    }

    @objc func applicationDidBecomeActive(_ notification: Notification) {
        guard timerEndTime != nil else {
            return
        }
        subtractTime()
    }

    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        stopTimerAndResetPrompt()
        removeNavigationLogo()
    }

    func showNavigationLogo() {
        if let logoView = logoView {
            updateNavigationLogoFrame()
            if logoView.superview == nil {
                navigationController?.view.addSubview(logoView)
            }
            navigationController?.view.bringSubviewToFront(logoView)
        }
    }

    func updateNavigationLogoFrame() {
        if let logoView = logoView {
            logoView.frame.origin.x = (view.bounds.width - logoView.frame.width) / 2
            logoView.frame.origin.y = 20
        }
    }

    func removeNavigationLogo() {
        logoView?.removeFromSuperview()
    }

    func setupAccessibility() {
        seconds.accessibilityLabel = "Brushing timer"
        seconds.accessibilityValue = seconds.text
        brushBtn.accessibilityLabel = "Start brushing timer"
        brushBtn.accessibilityHint = "Starts a two minute brushing countdown"
        brushText.accessibilityLabel = "Brushing reminder"
    }

    func updateTimerLabel() {
        let labelText = "\(second) seconds"
        seconds.text = labelText
        seconds.accessibilityValue = labelText
    }

    func stopTimerAndResetPrompt() {
        timer?.invalidate()
        timer = nil
        timerEndTime = nil
        second = 0
        updateTimerLabel()
        brushText.layer.removeAllAnimations()
        brushText.alpha = 0
        brushBtn.isHidden = false
        brushText.isHidden = true
    }
}
