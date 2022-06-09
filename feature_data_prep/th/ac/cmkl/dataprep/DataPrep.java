/*   DataPrep.java
 *
 *   This is a GUI application to gather feature data for the machine learning lab.
 *   Created by Sally Goldin, 8 June 2022
 *   Copyright 2022 by CMKL University
 */
package th.ac.cmkl.dataprep;
 
import javax.swing.*;
import javax.swing.border.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;
import java.io.*;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.net.URISyntaxException;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * Main class for DataPrep application. Defines the GUI and controls the flow.
 */
public class DataPrep extends JFrame 
                       implements ActionListener,ItemListener
{
    /** User's nickname, used to create the file name */
    public static String nickname;
    
    /** Image directory - entered as argument */
    public static String imagePath;
    
    /** holds entered values for the current image */
    private ImageData currentImageData = null;
    
    /** Object to use for writing to the CSV file */
    private FileWriter csvWriter = null;
    
    /** Name of CSV file */
    private String csvFilename = "";
    
    /* values for populating drop down lists and offering choices */
    private static String[] petalColors = {"--","White", "Yellow", "Orange","Red","Pink","Purple","Blue","Other"};
    private static String[] petalShapes = {"--","Circle","Wide Ellipse","Narrow Ellipse","Jagged Edges"};
    private static String[] leafSizes = {"--","Large","Medium","Small","No leaves visible"};
    
    /**
     * Randomly ordered collection of image file names
     */
    private ArrayList<String> imageFileNames = new ArrayList<String>();

    /**
     * Current index in the image files array list. Updated by the 'Next' button 
     */
    private int imageIndex = 0; 
    
    /* UI controls */
    private JButton nextButton;
    private JButton exitButton;
    private JComboBox<String> colorList;
    private JComboBox<String> shapeList;
    private JComboBox<String> leafList;
    private JRadioButton yesButton;
    private JRadioButton noButton;
    private JLabel imageDisplayLabel;
    private ButtonGroup buttonGroup;
    
    /**
      * Constructor creates the User Interface.
      */
    public DataPrep()
    {
      super("ML Data Preparation Application");
      imageFileNames = new ArrayList<String>();
      buildUI();
      //String imagePath = getImageDirectoryPath();
      setupImageList(imagePath);
      writeCsvHeader();
    }

    /**
     * Create the GUI and link to listeners
     */
    private void buildUI()
    {
      JPanel mainPanel = new JPanel(new BorderLayout());
      mainPanel.setBorder(new EmptyBorder(10,10,10,10));
      JPanel imagePanel = new JPanel(new BorderLayout());
      JPanel innerImagePanel = new JPanel(new FlowLayout());
      innerImagePanel.setPreferredSize(new Dimension(640,400));
      imagePanel.setBorder(new EtchedBorder());
      imagePanel.add(innerImagePanel,BorderLayout.CENTER);
      JPanel inputPanel = new JPanel(new GridLayout(0,2,20,20));
      JPanel inputPanelFrame = new JPanel(new BorderLayout());
      inputPanelFrame.setBorder(new EmptyBorder(20,20,20,20));
      JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,20,10));
      inputPanelFrame.add(inputPanel,BorderLayout.CENTER);
      
      imageDisplayLabel = new JLabel();
      innerImagePanel.add(imageDisplayLabel);
      
      mainPanel.add(imagePanel,BorderLayout.NORTH);
 
      inputPanel.add(new JLabel("Main color of petals"));
      colorList = createComboBox(petalColors);
      colorList.addItemListener(this);
      inputPanel.add(colorList);
      
      inputPanel.add(new JLabel("Petal shape"));
      shapeList = createComboBox(petalShapes);
      shapeList.addItemListener(this);
      inputPanel.add(shapeList);
 
      inputPanel.add(new JLabel("Leaf size (relative to petals)"));
      leafList = createComboBox(leafSizes);
      leafList.addItemListener(this);
      inputPanel.add(leafList);
      
      inputPanel.add(new JLabel("Is the calyx visible? (former bud at the base of the flower)"));
      yesButton = new JRadioButton("Yes");
      yesButton.addActionListener(this);
      noButton = new JRadioButton("No");
      noButton.addActionListener(this);
      buttonGroup = new ButtonGroup();
      buttonGroup.add(noButton);
      buttonGroup.add(yesButton);

      JPanel radioPanel = new JPanel(new FlowLayout());
      radioPanel.add(noButton);
      radioPanel.add(yesButton);
      inputPanel.add(radioPanel);
           
      mainPanel.add(inputPanelFrame,BorderLayout.CENTER);
      
      nextButton = new JButton("Next");
      nextButton.addActionListener(this); 
      buttonPanel.add(nextButton);
      exitButton = new JButton("Exit");
      exitButton.addActionListener(this);
      buttonPanel.add(exitButton);
      mainPanel.add(buttonPanel,BorderLayout.SOUTH);
    
      getContentPane().add(mainPanel, BorderLayout.CENTER);

    }

    /** 
     * Create a combo box and populate it with strings drawn from the passed array.
     * @param   comboValues      String array to populate combo box
     * @return  new combo box with choices initialized
     */
    private JComboBox<String> createComboBox(String[] comboValues)
    {
	JComboBox<String> newCombo = new JComboBox<String>();
	for (String option : comboValues)
	{
	    newCombo.addItem(option);
	}
	return newCombo;
    }
     
    /** 
     * This is the method required for the ActionListener 
     * interface. It handles the necessary actions when 
     * buttons are pressed.
     */
    public void actionPerformed(ActionEvent e)
    {
	Object source = e.getSource();
	if (source == exitButton)
	{
	    doExit();
	}
	else if (source == nextButton)
	{
	    // Check that all data has been entered
	    // Save in the file 
	    // Also need to reset the controls to defaults
	    if (imageIndex + 1 >= imageFileNames.size())
	    {
		doExit();
	    }
	    else
	    {
		if (currentImageData != null)
		{
		    if (currentImageData.isDataComplete())
		    {
			try 
			{
			    csvWriter.write(currentImageData.getCsvFileLine());
			    csvWriter.flush();
			}
			catch (IOException ioe)
			{
			    JOptionPane.showMessageDialog(this, 
			      "Error writing to output file "+ csvFilename, "File Error", JOptionPane.ERROR_MESSAGE); 
			    System.exit(1);
			}
		    	imageIndex += 1;
			displayImage(imageIndex);
			resetControls();
		    }
		    else
		    {
			JOptionPane.showMessageDialog(this, 
			"Please enter values for all features", "Incomplete Information", JOptionPane.ERROR_MESSAGE); 
		    }
		}
	    }
	}
	else if (source == noButton)
	{
	    if ((noButton.isSelected()) && (currentImageData != null))
		currentImageData.setBudVisible(false);
		
	}
	else if (source == yesButton)
	{
	    if ((yesButton.isSelected()) && (currentImageData != null))
		currentImageData.setBudVisible(true);
		
	}
    }
    
    /** 
     * Centralize cleanup processing during exit.
     */
    private void doExit()
    {
	try
	{
	    csvWriter.close();
	}
	catch (IOException e)
	{
	    // ignore problem on close
	}
	JOptionPane.showMessageDialog(this, 
			"Exiting the program.\nFeature data saved in file: "+ csvFilename, 
			"Exiting", JOptionPane.PLAIN_MESSAGE); 
	System.exit(0);
    }
    
    /**
     * Method required for itemListener implementation.
     * Handles the correct action when an item is selected
     */
    public void itemStateChanged(ItemEvent e)
    {	
	Object source = e.getSource();
	int idx = 0; 
	if (e.getStateChange() != ItemEvent.SELECTED)
	    return;
	if (currentImageData == null)
	    return;
	if (source == colorList)
	{
	    idx = colorList.getSelectedIndex();
	    if (idx > 0)
		currentImageData.setBlossomColor(idx);
	}
	else if (source == shapeList)
	{
	    idx = shapeList.getSelectedIndex();
	    if (idx > 0)
		currentImageData.setBlossomShape(idx);
	}
	else if (source == leafList)
	{	    
	    idx = leafList.getSelectedIndex();
	    if (idx > 0)
		currentImageData.setLeafSize(idx);
	}
    }
    
    /**
     * Populate the array list of image files with the contents of the
     * images directory
     * @argument   directory  Relative path of the images
     */
     private void setupImageList(String directory)
     {
	File folder = new File(directory);
	File[] listOfFiles = folder.listFiles();
	if ((listOfFiles == null) || (listOfFiles.length == 0))
	{
	    JOptionPane.showMessageDialog(this, 
			"Invalid image path "+ directory, "Invalid Path", JOptionPane.ERROR_MESSAGE); 
	    System.exit(1);
	}
	for (File f : listOfFiles)
	{
	    if (f.isFile())
	    {
		String filename = f.getAbsolutePath();
		if (filename.endsWith(".jpg") || filename.endsWith(".png"))
		    imageFileNames.add(f.getAbsolutePath());
	    }
	}
	if (imageFileNames.size() == 0)
	{
	    JOptionPane.showMessageDialog(this, 
			"No images found in "+ directory, "No images found", JOptionPane.ERROR_MESSAGE); 
	    System.exit(1);
	}	
	/* randomize the order */
	Collections.shuffle(imageFileNames,new Random(System.currentTimeMillis()));
     }
     
     /**
      * Use reflection to figure out the path where the
      * image files are stored.
      * By convention they will be at the top level of the jar
      * in a subdirectory called "images"
      * @return  absolute path to the images
      */
     private String getImageDirectoryPath()
     {
	try 
	{
	    String jarPath = DataPrep.class
		      .getProtectionDomain()
		      .getCodeSource()
		      .getLocation()
		      .toURI()
		      .getPath();
	    return jarPath + "images";  // jarPath already has a separator
	}
	catch (URISyntaxException e)
	{
	    return new String("");
	}
     }

     /** 
      * Use ImageIO to read and display an image from the array list.
      * Public so it can be called by main() during initialization.
      * @param index    Numeric index into the array list
      */
     public void displayImage(int index)
     {
	if ((index < 0) || (index >= imageFileNames.size()))
	{
	    System.out.println("Invalid image index - out of range: " + index);
	    return;
	}
	try 
	{
	    String fname = imageFileNames.get(index);
	    BufferedImage img = ImageIO.read(new File(fname));
	    imageDisplayLabel.setIcon(new ImageIcon(img));
	    currentImageData = new ImageData(fname);
	    currentImageData.setFlowerCategory(getCategory(fname));
	}
	catch (IOException e)
	{
	      JOptionPane.showMessageDialog(this, 
			"Error reading image file "+ imageFileNames.get(index), 
			"File Error", JOptionPane.ERROR_MESSAGE); 
	      System.exit(1);
	}
     }  
     
     /** 
      * get the category - 1 = tulip, 2 = carnation, 3 = daisy.
      * @param fname    Name of the file
      * @return 1,2,3 depending on the name, 0 if no match
      */
      private int getCategory(String fname)
      {
	  String basename = "";
	  Path path = Paths.get(fname);
	  basename = path.getFileName().toString();

	  int category = 0;
	  if (basename.startsWith("tulip"))
	      category = 1;
	  else if (basename.startsWith("carn"))
	      category = 2;
	  else if (basename.startsWith("dais"))
	      category = 3;
	  return category;
      }
     
     /** 
      * Reset the controls after showing a new image
      */
      private void resetControls()
      {
          buttonGroup.clearSelection();
	  colorList.setSelectedIndex(0);
	  shapeList.setSelectedIndex(0);
	  leafList.setSelectedIndex(0);         
      }
     
 
     /** 
      * Create a file writer for the output file and
      * write a line of column headings. This function can
      * fail, in which case the program will exit.
      */
      private void writeCsvHeader()
      {
	  csvFilename = nickname + "_features.csv";
	  try 
	  {  
	      csvWriter = new FileWriter(csvFilename);
	      csvWriter.write(ImageData.getHeaderLine());
	      csvWriter.flush();
	  } 
	  catch (IOException e) 
	  {
	      JOptionPane.showMessageDialog(this, 
			"Cannot open output file "+ csvFilename, "File Error", JOptionPane.ERROR_MESSAGE); 
	      System.exit(1);
	  } 
      }
     
    /**
     * Driver to start the application running.
     */	
    public static void main(String args[])
     {		      
     try
        {
        UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
	}
     catch (Exception ex)
        {
        System.out.println("Error setting look and feel!");
        System.exit(1);
        }
     if (args.length < 2)
     {
	JOptionPane.showMessageDialog(null, 
			"Missing arguments. Usage:\n\n" +
			" java -cp DataPrep.jar th.ac.cmkl.dataprep.DataPrep [nickname] [imagedir]\n\n", 
			"Missing argument", JOptionPane.ERROR_MESSAGE);
	System.exit(0);
	
     }
     nickname = args[0];
     imagePath = args[1];
     DataPrep app = new DataPrep();
     app.pack();
     // center the application 
     app.setVisible(true);
     app.displayImage(0);
     }     
}