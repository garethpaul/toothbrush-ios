//
//  ViewController.swift
//  toothbrush
//
//  Created by Gareth on 5/23/15.
//  Copyright (c) 2015 GarethPaul. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBAction func start(sender: AnyObject) {
        setupTimer()
        brushBtn.hidden = true
        brushText.hidden = false
    }
    
    @IBOutlet weak var seconds: UILabel!
    @IBOutlet weak var brushBtn: UIButton!
    @IBOutlet weak var brushText: UILabel!
    
    var timer = NSTimer()
    var second = 0
    var count = 0
    var logoView: UIImageView!

    deinit {
        timer.invalidate()
        removeNavigationLogo()
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        
        logoView = UIImageView(frame: CGRectMake(0, 0, 40, 40))
        logoView.image = UIImage(named: "logo")?.imageWithRenderingMode(.AlwaysTemplate)
        logoView.tintColor = toColor("#EA0796")
        logoView.frame.origin.x = (self.view.frame.size.width - logoView.frame.size.width) / 2
        logoView.frame.origin.y = 20
        
        self.navigationController?.navigationBar.barTintColor = toColor("#F6EC28")

        showNavigationLogo()
        setupAccessibility()

        // Do any additional setup after loading the view, typically from a nib.
    }

    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        showNavigationLogo()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func setupTimer()  {
        timer.invalidate()
        second = 120
        count = 0

        updateTimerLabel()
        
        timer = NSTimer.scheduledTimerWithTimeInterval(1.0, target: self, selector: Selector("subtractTime"), userInfo: nil, repeats: true)
        timer.tolerance = 0.1
        NSRunLoop.mainRunLoop().addTimer(timer, forMode: NSRunLoopCommonModes)
        brushText.layer.removeAllAnimations()
        brushText.alpha = 0
        UIView.animateWithDuration(0.5, delay: 0.5, options: [UIViewAnimationOptions.Repeat, UIViewAnimationOptions.Autoreverse], animations: { () -> Void in
            self.brushText.alpha = 1
        }, completion: nil)
        
        
        
    }

    func subtractTime() {
        second--

        if(second <= 0)  {
            second = 0
            stopTimerAndResetPrompt()
        }

        updateTimerLabel()
    }

    override func viewWillDisappear(animated: Bool) {
        super.viewWillDisappear(animated)
        stopTimerAndResetPrompt()
        removeNavigationLogo()
    }

    func showNavigationLogo() {
        if let logoView = logoView {
            if logoView.superview == nil {
                self.navigationController?.view.addSubview(logoView)
            }
            self.navigationController?.view.bringSubviewToFront(logoView)
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
        timer.invalidate()
        second = 0
        updateTimerLabel()
        brushText.layer.removeAllAnimations()
        brushText.alpha = 0
        brushBtn.hidden = false
        brushText.hidden = true
    }

}
