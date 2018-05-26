//
//  HomeNewsViewContrller.swift
//  Wasabi
//
//  Created by 1002237 on 2018. 5. 12..
//  Copyright © 2018년 1002237. All rights reserved.
//

import UIKit
import SwiftyJSON


private let textCellId = "TextNewsCell"
private let imageCellId = "ImageNewsCell"

class HomeNewsViewContrller: UICollectionViewController {

    var jsonNews:JSON?
    override func viewDidLoad() {
        super.viewDidLoad()


        let path = Bundle.main.path(forResource: "news", ofType: "json")!
        let jsonString = try? String(contentsOfFile: path, encoding: String.Encoding.utf8)
        jsonNews = JSON(parseJSON: jsonString!)

        let titleLabel = UILabel(frame: CGRect(x: 10, y: 10, width: UIScreen.main.bounds.width, height: 100))
        titleLabel.text = "News"
        titleLabel.textColor = UIColor.white
        titleLabel.font = UIFont.systemFont(ofSize: 20.0)
        titleLabel.backgroundColor = UIColor.red
        navigationItem.titleView = titleLabel
        
        
        self.collectionView?.reloadData()
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
        // Get the new view controller using [segue destinationViewController].
        // Pass the selected object to the new view controller.
    }
    */

    // MARK: UICollectionViewDataSource

    override func numberOfSections(in collectionView: UICollectionView) -> Int {
        // #warning Incomplete implementation, return the number of sections
        return 1
    }


    override func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        // #warning Incomplete implementation, return the number of items
        return jsonNews?.dictionary?["news"]?.array?.count ?? 0
    }

    override func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        var isImageCell:Bool = false
        if let imageUrlString = jsonNews?.dictionary?["news"]?.array?[indexPath.row].dictionary?["image_url"]?.stringValue, imageUrlString.count > 0 {
            isImageCell = true
        }
        
        let cell:UICollectionViewCell?
        if isImageCell{
            let imgCell = collectionView.dequeueReusableCell(withReuseIdentifier: imageCellId, for: indexPath) as? ImageNewsCell
            imgCell?.load(newsItem: (jsonNews?.dictionary?["news"]?.array?[indexPath.row])!)
            cell = imgCell
        }else{
            let textCell = collectionView.dequeueReusableCell(withReuseIdentifier: textCellId, for: indexPath) as? TextNewsCell
            textCell?.load(newsItem: (jsonNews?.dictionary?["news"]?.array?[indexPath.row])!)
            cell = textCell
        }
    
        return cell!
    }

    // MARK: UICollectionViewDelegate

    override func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath){
        
        if let urlString = jsonNews?.dictionary?["news"]?.array?[indexPath.row]["link_url"].stringValue{
            navigationController?.pushViewController(NewsDetailViewController(urlString: urlString), animated: true)
        }
        
    }
    /*
    // Uncomment this method to specify if the specified item should be highlighted during tracking
    override func collectionView(_ collectionView: UICollectionView, shouldHighlightItemAt indexPath: IndexPath) -> Bool {
        return true
    }
    */

    /*
    // Uncomment this method to specify if the specified item should be selected
    override func collectionView(_ collectionView: UICollectionView, shouldSelectItemAt indexPath: IndexPath) -> Bool {
        return true
    }
    */

    /*
    // Uncomment these methods to specify if an action menu should be displayed for the specified item, and react to actions performed on the item
    override func collectionView(_ collectionView: UICollectionView, shouldShowMenuForItemAt indexPath: IndexPath) -> Bool {
        return false
    }

    override func collectionView(_ collectionView: UICollectionView, canPerformAction action: Selector, forItemAt indexPath: IndexPath, withSender sender: Any?) -> Bool {
        return false
    }

    override func collectionView(_ collectionView: UICollectionView, performAction action: Selector, forItemAt indexPath: IndexPath, withSender sender: Any?) {
    
    }
    */

}

extension HomeNewsViewContrller : UICollectionViewDelegateFlowLayout{
    public func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize{
        return CGSize(width: self.view.frame.width, height: 290)
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumLineSpacingForSectionAt section: Int) -> CGFloat {
        return 5
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, insetForSectionAt section: Int) -> UIEdgeInsets{
        return UIEdgeInsets(top: 5, left: 0, bottom: 0, right: 0)
    }
}
