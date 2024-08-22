import React from 'react';
import './list_before_interview.css';
interface ImageContainerProps {
    onActivate: () => void;
  }
  const ImageContainer: React.FC<ImageContainerProps> = ({ onActivate }) => {
    return (
        <form id="interview-form">
            <div className="lists_row">
                <div className="list">
                    <h2>學校</h2>
                    <ul className="school-list scrollable-list">
                        <label><input type="radio" id="school1" name="school" value="國立台灣大學" required /> 國立台灣大學</label>
                        <label><input type="radio" id="school2" name="school" value="國立清華大學" /> 國立清華大學</label>
                        <label><input type="radio" id="school3" name="school" value="國立交通大學" /> 國立交通大學</label>
                        <label><input type="radio" id="school4" name="school" value="國立成功大學" /> 國立成功大學</label>
                        <label><input type="radio" id="school5" name="school" value="國立政治大學" /> 國立政治大學</label>
                        <label><input type="radio" id="school6" name="school" value="國立中央大學" /> 國立中央大學</label>
                        <label><input type="radio" id="school7" name="school" value="國立台灣師範大學" /> 國立台灣師範大學</label>
                    </ul>
                </div>
                <div className="list">
                    <h2>科系</h2>
                    <ul className="department-list scrollable-list">
                        <label><input type="radio" id="department1" name="department" value="管理科學系" required /> 管理科學系</label>
                        <label><input type="radio" id="department2" name="department" value="資訊管理與財務金融學系" />資訊管理與財務金融學系</label>
                        <label><input type="radio" id="department3" name="department" value="工業工程與管理學系" />工業工程與管理學系</label>
                        <label><input type="radio" id="department4" name="department" value="運輸與物流管理學系" />運輸與物流管理學系</label>
                        <label><input type="radio" id="department5" name="department" value="生物科技學系" />生物科技學系</label>
                        <label><input type="radio" id="department6" name="department" value="應用化學系" />應用化學系</label>
                        <label><input type="radio" id="department7" name="department" value="電子物理學系" />電子物理學系</label>
                    </ul>
                </div>
                <div className="list">
                    <h2>履歷上傳</h2>
                    <label className="upload-button">
                        <input type="file" id="file" name="file" accept="application/pdf" required />
                        <img src="{{ url_for('static', filename='images/upload-icon.png') }}" alt="Upload Icon" />
                    </label>
                </div>
            </div>

            <div className="button-container">
                <div>
                    <button className="btn" >退出</button>
                </div>
                <div>
                    <button className="btn" type="button" onClick={onActivate}>啟動</button> {/* Trigger activate on click */}
                </div>
            </div>
        </form>
    );
};

export default ImageContainer;
