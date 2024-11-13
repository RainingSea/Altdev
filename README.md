## Hub for the paper "AltDev: Multi-Agent Software Development via Real-Time Alignment"

### Tutorial

```
├─0_config
├─agents 
├─align_flow # the alignment control process for agents other than the programmer.
├─messages
├─model # base model of project
├─project_dir # dir of generated projects
├─prompt # including each agent's generating prompt and alignment prompt
├─utils

```

### Generating Process

The prompts for the generation process of each agent are stored in the corresponding action files within the **prompt** folder.

### Alignment Process

The prompts for the alignment process (including checking and multi agent debate) of each agent are stored in the **align_prompt.py** file within the **prompt** folder.

#### Alignment Process Control

1. First, in the **/agents/team.py** file, specify which roles will undergo the alignment process. The operation involves designating the target role for the **self.roles[Reviewer]** and then executing this reviewer.

   > for example, the code to activate alignment process for Architect is 
   >
   > ```python
   > self.roles["Reviewer"].target = self.roles["Architect"]
   > self.roles["Reviewer"].go()
   > ```

2. Second, also in the **/agents/team.py** file, specify the number of alignment checking and the number of multi agents discussion rounds. Set the values for these two variables: **align_check_num** and **mad_num**

3. Finally, the control of the alignment process involves two files: one is **align_flow/align_flow.py** file in folder A, which controls the alignment process for all agents other than the programmer.  The other is **agents/programmer.py**, due to the complexity of the programmer's process, it has been extracted separately.

   
