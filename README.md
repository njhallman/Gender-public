This code creates the paper at https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4678211 

## Setup Instructions

### Prerequisites

- **A large amount of RAM (at least 64GB, but even that might crash. I ran this on an M4 Mac with 128 GB of memory)**
- **Docker** installed ([Get Docker](https://docs.docker.com/get-docker/)). Make sure to edit the settings so that Docker has access to enough RAM - the default is normally only a few GB. 
- **VS Code** with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Running the Project with Dev Containers

1. **Clone the repository**:

   ```sh
   git clone https://github.com/njhallman/Gender.git
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

## Usage

### Running the Analysis
Once you have the project open in the container, you can open and run the jupyter notebook at /Analysis/Code/Pull Data from WRDS and Conduct Analysis.ipynb. This file will download the required data from Revelio via WRDS and perform all the analysis in the paper, including all the tables and figures. You will be prompted to provide your WRDS login credentials, and the code will only work properly if your WRDS account has access to Revelio data. Note that the version of the Revelio data you download will be newer than the version used to produce the tables and figures in the publicly available version of the paper, and will therefore produce a (hopefully only slightly) different set of tables and figures. 

### Compiling the Paper
The paper is written in LaTeX. All the LaTeX files required to produce the paper are included in the LaTeX directory in the repo. Running /Analysis/Code/Pull Data from WRDS and Conduct Analysis.ipynb will replace the tables and figures in the LaTeX/Tables and LaTeX/Figures directories, which will be reflected in newly compiled versions of the paper. 
