/*   ImageData.java
 *
 *   Part of the DataPrep application
 *   Class to hold information about one image
 *   Created by Sally Goldin, 8 June 2022
 *   Copyright 2022 by CMKL University
 */

package th.ac.cmkl.dataprep;

import java.util.*;
import java.text.SimpleDateFormat;
import java.sql.Timestamp;

/**
 * An instance of this class is created for each image the user describes.
 * It has setters to set the different data fields, plus methods
 * to transform it to a line to be written in a CSV file.
 */
public class ImageData {

    /** Name of the image being described */
    private String imageFile;
    
    /** Category of the image - 1 is tulip, 2 is carnation, 3 is daisy */
    private int flowerCategory;
    
    /** Blossom color */
    private int blossomColor;
    
    /** Blossom shape */
    private int blossomShape;
    
    /** Leaf size */
    private int leafSize;
    
    /** Is calyx visible - 1 is false, 2 is true */
    private int budVisible;
    
    private static final SimpleDateFormat sdf = new SimpleDateFormat("yyyy.MM.dd.HH.mm.ss");
    
    /**
     *  Constructor initializes the image file.
     *  Sets all other fields to empty
     */
     public ImageData(String filename)
     {
	imageFile = filename;
	flowerCategory = 0;
	blossomColor = 0;
	blossomShape = 0;
	leafSize = 0;
	budVisible = 0;
     }
    
 
    
     /** Setters for each field */
     public void setFlowerCategory(int value)
     {
	flowerCategory = value;
     }

     public void setBlossomColor(int value)
     {
	blossomColor = value;
     }

     public void setBlossomShape(int value)
     {
	blossomShape = value;
     }
     
     
     public void setLeafSize(int value)
     {
	leafSize = value;
     }
     
     public void setBudVisible(boolean value)
     {
	if (value)
	  budVisible = 2;
	else
	  budVisible = 1;
     }
     
     /** Check if all values have been set.
      * @return true if all have been set, else false.
      */
     public boolean isDataComplete()
     {
	boolean isComplete = true;
	if (blossomColor == 0)
	    isComplete = false;
	if (blossomShape == 0)
	    isComplete = false;
	if (leafSize == 0)
	    isComplete = false;
	if (budVisible == 0)
	    isComplete = false;    
	return isComplete;    
     }
     
     /**
      * Return a string that holds column headers
      */
     public static String getHeaderLine()
     {
	String header = "Image file name, Category, Color code, "+
	                "Shape code, Size code, Bud visible code, Timestamp\n";
	return header;
     }
     
     /** Return a comma delimited string that holds the data
      * Order: image name, category, color, shape, size, bud visible, timestamp
      * @return comma delimited string
      */
      public String getCsvFileLine()
      {
	  StringBuffer buffer = new StringBuffer();
	  buffer.append(imageFile + ",");
	  buffer.append(Integer.toString(flowerCategory) + ","); 
	  buffer.append(Integer.toString(blossomColor) + ","); 
	  buffer.append(Integer.toString(blossomShape) + ","); 
	  buffer.append(Integer.toString(leafSize) + ","); 
	  buffer.append(Integer.toString(budVisible) + ","); 	  	  	  	  
	  buffer.append(getTimestampString() + "\n");
	  return buffer.toString();
      }

      
      /**
       * @return current date and time as string
       */
      public String getTimestampString()
      {
      	  Date date = new Date();
	  Timestamp timestamp = new Timestamp(date.getTime());
	  return sdf.format(timestamp);
      }

      /**
       * Return a string with all the current values
       * @return String representation
       */
      public String toString()
      {
	  return "Color: " + blossomColor + "  Shape: " + blossomShape +
	      "  Size: " + leafSize + " Bud: " + budVisible;
      }
}