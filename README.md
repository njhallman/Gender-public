This code creates the paper at https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4678211 

## Setup Instructions

### Prerequisites

- **A large amount of RAM (I ran this on an M4 Mac with 128 GB of memory)**
- **Docker** installed ([Get Docker](https://docs.docker.com/get-docker/)). Make sure to edit the settings so that Docker has access to enough RAM - the default is normally only a few GB. 
- **VS Code** with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers). Cursor also works, as it is built on top of VSCode.  

### Running the Project with Dev Containers
1. **Clone the repository**:

   ```sh
   git clone https://github.com/njhallman/Gender-public.git
   cd repository-name
   ```

2. **Open the project in VS Code**.

3. **Add your Stata license information**
   - Create a file called `stata.lic' in the .devcontainer directory
   - Enter your Stata license information in the new stata.lic file. It should look something like: 123456789012!abc3 def5 ghi7 jkl9 mno2 $p4r stu6 vwx8 yz0!John Doe!Sample University!1234!

4. **"Reopen in Container"** (if not prompted, open the Command Palette in VS Code `Ctrl+Shift+P` and select:  
   `"Dev Containers: Reopen in Container"`).

4. The **development container** will build automatically. This setup includes:
   - **Python** (with dependencies from `requirements.txt`)
   - **Stata**
   - **LaTeX** (for compiling the manuscript)
   - **VS Code extensions** (e.g., LaTeX Workshop, Python)

Once the container is running, all required dependencies should be installed automatically. If VSCode asks to install additional extensions in the container, you should allow it to do so. 

---

## Directory Structure

The project is organized into the following main directories:

### /Analysis
- `/Code`: Contains Python and Jupyter notebook files for data processing and analysis
  - `download_data.py`: Script to download raw data from WRDS
  - `conduct_analysis.ipynb`: Main analysis notebook that processes data and generates results
- `/Data`: Raw and processed data files (not included in repo)
  - Data will be downloaded here when running `download_data.py`

### /LaTeX
- `/Tables`: Generated tables from the analysis
- `/Figures`: Generated figures from the analysis
- Main LaTeX source files for the paper

### /.devcontainer
- Development container configuration files
- `stata.lic`: Location for your Stata license file (not included in repo)

### /.vscode
- VS Code workspace settings and configurations
- Container-specific VS Code settings

---

## Usage

### Running the Analysis
Once you have the project open in the container, you can download the data required to perform the analysis from WRDS by running /Analysis/Code/download_data.py. You will be prompted to provide your WRDS login credentials, and the code will only work properly if your WRDS account has access to Revelio data. Note that the version of the Revelio data you download will be newer than the version used to produce the tables and figures in the publicly available version of the paper, and will therefore produce a (hopefully only slightly) different set of tables and figures. 

Once the data is downloaded you can run /Analysis/Code/conduct_analysis.ipynb, which will prepare the raw data for analysis and then conduct the analysis described in the paper, including creating all tables and figures from the paper.

#### Using tmux
You may (or may not) find it useful to use tmux to run these programs. The commands are: 
   
   1. To download the data: 
      ```sh
      tmux new-session -d -s download "bash -c 'python3 /workspaces/gender-public/Analysis/Code/download_data.py || read -p \"Press enter to close...\"'"
      ```
   
   2. To conduct the analysis: 
      ```sh
      tmux new-session -d -s analysis "bash -c 'jupyter nbconvert --to script --stdout /workspaces/gender-public/Analysis/Code/conduct_analysis.ipynb | python3; read -p \"Press enter to close...\"'"
      ```

### Compiling the Paper
The paper is written in LaTeX. All the LaTeX files required to produce the paper are included in the LaTeX directory in the repo. Running /Analysis/Code/conduct_analysis.ipynb will replace the tables and figures in the LaTeX/Tables and LaTeX/Figures directories, which will be reflected in newly compiled versions of the paper.




---






