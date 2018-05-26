//
//  ImageNewsCellCollectionViewCell.swift
//  Wasabi
//
//  Created by 1002237 on 2018. 5. 27..
//  Copyright © 2018년 1002237. All rights reserved.
//

import UIKit
import SwiftyJSON
class ImageNewsCell: UICollectionViewCell {
    @IBOutlet weak var titleLabel: UILabel!
    @IBOutlet weak var imageView: UIImageView!
    func load(newsItem:JSON){
        titleLabel.text = newsItem.dictionary?["title"]?.stringValue
        
        if let urlString = newsItem.dictionary?["image_url"]?.stringValue , urlString.count > 0{
            do{
                let data = try Data(contentsOf:URL(string: urlString)!)
                imageView.image = UIImage(data: data)
            }catch{
                
            }
        }
    }
}
