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
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        logoView = UIImageView(frame: CGRectMake(0, 0, 40, 40))
        logoView.image = UIImage(named: "logo")?.imageWithRenderingMode(.AlwaysTemplate)
        logoView.tintColor = toColor("#EA0796")
        logoView.frame.origin.x = (self.view.frame.size.width - logoView.frame.size.width) / 2
        logoView.frame.origin.y = 20
        
        // Add the logo view to the navigation controller.
        self.navigationController?.view.addSubview(logoView)
        
        // Bring the logo view to the front.
        self.navigationController?.view.bringSubviewToFront(logoView)
        self.navigationController?.navigationBar.barTintColor = toColor("#F6EC28")

        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func setupTimer()  {
        second = 120
        count = 0

        seconds.text = "\(second) seconds"
        
        timer = NSTimer.scheduledTimerWithTimeInterval(1.0, target: self, selector: Selector("subtractTime"), userInfo: nil, repeats: true)
        brushText.alpha = 0
        UIView.animateWithDuration(0.5, delay: 0.5, options: [UIViewAnimationOptions.Repeat, UIViewAnimationOptions.Autoreverse], animations: { () -> Void in
            self.brushText.alpha = 1
        }, completion: nil)
        
        
        
    }

    func subtractTime() {
        second--
        seconds.text = "\(second) seconds"
        
        if(second == 0)  {
            timer.invalidate()
            brushBtn.hidden = false
            brushText.hidden = true
        }
    }

    
}

