//
//  NewsDetailViewController.swift
//  Wasabi
//
//  Created by 1002237 on 2018. 5. 26..
//  Copyright © 2018년 1002237. All rights reserved.
//

import UIKit
import WebKit

class NewsDetailViewController: UIViewController {

    private var urlString:String?
    convenience init(urlString:String){
        self.init()
        self.urlString = urlString
    }
    
    private lazy var webView: WKWebView = {
        let conf = WKWebViewConfiguration()
        let webView = WKWebView(frame: self.view.bounds, configuration: conf)
        
        if let urlString = self.urlString , let url = URL(string:urlString) {
            let req = URLRequest(url: url)
            webView.load(req)
        }
        
        return webView
    }()
    override func viewDidLoad() {
        super.viewDidLoad()
        self.view.backgroundColor = .white
//        navigationItem.hidesBackButton = true
        
        let titleLabel = UILabel(frame: CGRect(x: 10, y: 10, width: UIScreen.main.bounds.width, height: 100))
        titleLabel.text = "News Detail"
        titleLabel.textColor = UIColor.white
        titleLabel.font = UIFont.systemFont(ofSize: 20.0)
        titleLabel.backgroundColor = UIColor.red
        navigationItem.titleView = titleLabel
        
        self.view.addSubview(webView)

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
