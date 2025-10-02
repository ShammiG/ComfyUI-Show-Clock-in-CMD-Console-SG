# ComfyUI-Show-Clock-in-CMD-Console-SG


Simple node that automatically intializes at ComfyUI startup. **No extra dependencies needed**.
This eliminates the need to add a Node to every workflow.
<img width="1892" height="77" alt="Startup" src="https://github.com/user-attachments/assets/6cdba341-fb40-432d-a8be-1dbacc7f8d7d" /> 


**Shows 24H clock time in CMD Console** when :
**Process starts**, Process **ends**, if Process is **interrupted** (both through UI and with Ctrl+C) and if Process **fails**         

Also useful when there are several processes in queue and you want to find out at what specific time did certain process started or ended.         
        
**Color coded** for easier viewing, this also makes it easier finding any earlier interruptions or Processes in console.
                  
Processing time is displayed in **Minutes and seconds** even if process takes less than 10 minutes (By default, comfyUI shows only in seconds if processing takes less than 10 minutes.)           

               
**General :**
<img width="1904" height="225" alt="proccesing begins and fisnished" src="https://github.com/user-attachments/assets/4c1128f0-25d7-4eeb-8371-b6f344a2796c" />

**When Interrupted with ComfyUI :**
<img width="1887" height="145" alt="interruped comfy" src="https://github.com/user-attachments/assets/cbfc6a0e-cfde-4701-bb8f-76f38c1f9c8a" />

**When Interrupted from console with Ctrl+C :**
<img width="1899" height="92" alt="interupt from cmd" src="https://github.com/user-attachments/assets/50132061-7260-478e-ad95-f6d78d99c7c2" />

**If processing fails for some reason :**
<img width="1903" height="106" alt="fails" src="https://github.com/user-attachments/assets/1c8b1e84-9c40-48c1-b31a-23d382a63ed1" />



# Installation:
**1.** Clone this repository into your **ComfyUI/custom_nodes** directory:    
       
               git clone https://github.com/ShammiG/ComfyUI-Show-Clock-in-CMD-Console-SG.git  
      
**2.** **Restart ComfyUI**   
      
That's it. You will see the message during comfyUI startup in console:       
              
<img width="1892" height="77" alt="Startup" src="https://github.com/user-attachments/assets/fe3190c6-b027-4c71-be1d-f68aaa9fb2e8" />

