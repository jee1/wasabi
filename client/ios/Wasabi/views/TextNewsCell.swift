//
//  TextNewsCell.swift
//  Wasabi
//
//  Created by 1002237 on 2018. 5. 12..
//  Copyright © 2018년 1002237. All rights reserved.
//

import UIKit
import SwiftyJSON
class TextNewsCell: UICollectionViewCell {
    @IBOutlet weak var titleLabel: UILabel!
    @IBOutlet weak var summaryLabel: UILabel!
    func load(newsItem:JSON){
        titleLabel.text = newsItem.dictionary?["title"]?.stringValue
        summaryLabel.text = newsItem.dictionary?["contents"]?.stringValue
    }
}
