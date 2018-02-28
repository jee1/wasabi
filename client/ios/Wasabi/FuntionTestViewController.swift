//
//  ViewController.swift
//  Wasabi
//
//  Created by 1002237 on 2018. 2. 23..
//  Copyright © 2018년 1002237. All rights reserved.
//

import UIKit
import RxSwift
import RxCocoa
import AVFoundation



class FuntionTestViewController: UIViewController {

    @IBOutlet weak var functionTableView: UITableView!
    override func viewDidLoad() {
        super.viewDidLoad()
        self.functionTableView.delegate = self
        self.functionTableView.dataSource = self
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
}

extension FuntionTestViewController : UITableViewDelegate {
}

extension FuntionTestViewController : UITableViewDataSource{
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        return self.functionTableView.dequeueReusableCell(withIdentifier: "TTSCell")!
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int{
        return 1
    }
}

class TTSCell : UITableViewCell{
    @IBOutlet weak var playButton: UIButton!
    @IBOutlet weak var ttsTestLabel: UILabel!
    
    @IBAction func touchUpInsidePlayButton(_ sender: UIButton) {
        let synthesizer = AVSpeechSynthesizer()
        
        let utterance = AVSpeechUtterance(string: self.ttsTestLabel.text ?? "")
        utterance.voice = AVSpeechSynthesisVoice(language: "ko-KR")
        utterance.rate = 0.4
        
        synthesizer.speak(utterance)
    }
}

