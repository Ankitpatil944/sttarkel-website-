import React from 'react';

interface FloatingIconProps {
  src: string;
  alt: string;
  width: number;
  height: number;
  left: string;
  top: string;
  rotate: string;
  stacked: boolean;
  stackedLeft?: string;
  stackedTop?: string;
  style?: React.CSSProperties;
}

const FloatingIcon: React.FC<FloatingIconProps> = ({
  src,
  alt,
  width,
  height,
  left,
  top,
  rotate,
  stacked,
  stackedLeft = '28%',
  stackedTop = '80%',
  style = {},
}) => {
  return (
    <div
      className="absolute transition-all duration-1000 ease-in-out will-change-transform pointer-events-none"
      style={{
        ...style,
        left: stacked ? stackedLeft : left,
        top: stacked ? stackedTop : top,
        transform: stacked ? 'translate(-50%, -50%) rotate(0deg)' : `rotate(${rotate})`,
        zIndex: stacked ? 50 : 10,
        width,
        height,
      }}
    >
      <img src={src} alt={alt} width={width} height={height} />
    </div>
  );
};

export default FloatingIcon;















// import React from 'react';

// interface FloatingIconProps {
//   src: string;
//   alt: string;
//   width: number;
//   height: number;
//   left: string;
//   top: string;
//   rotate: string;
//   stacked: boolean;
//   stackedLeft?: string; // New: custom stack X
//   stackedTop?: string;  // New: custom stack Y
// }

// const FloatingIcon: React.FC<FloatingIconProps> = ({
//   src,
//   alt,
//   width,
//   height,
//   left,
//   top,
//   rotate,
//   stacked,
//   stackedLeft,
//   stackedTop,
// }) => {
//   const computedLeft = stacked ? stackedLeft || '28%' : left;
//   const computedTop = stacked ? stackedTop || '80%' : top;
//   const computedTransform = stacked
//     ? 'translate(-50%, -50%) rotate(0deg)'
//     : `rotate(${rotate})`;

//   return (
//     <div
//       className="absolute transition-all duration-1000 ease-out"
//       style={{
//         left: computedLeft,
//         top: computedTop,
//         transform: computedTransform,
//         zIndex: stacked ? 50 : 10,
//       }}
//     >
//       <img
//         src={src}
//         alt={alt}
//         width={width}
//         height={height}
//         className="inline-block mx-2 align-middle border-gray-200 border-opacity-60 rounded-xl"
//         style={{ verticalAlign: 'middle' }}
//       />
//     </div>
//   );
// };

// export default FloatingIcon;
